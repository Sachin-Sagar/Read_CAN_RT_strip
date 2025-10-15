// fast_reader.c
#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <canlib.h>
#include <stdio.h>
#include <windows.h> // For Sleep and threading

// This struct will hold the state for our reader thread
typedef struct {
    int channel;
    long bitrate; // Use long for bitrate to match canSetBusParams
    int is_running;
    PyObject *queue; // A Python queue object to put messages into
} ReaderThreadState;

// The function that will run in our dedicated C thread
DWORD WINAPI reader_thread_func(LPVOID lpParam) {
    ReaderThreadState *state = (ReaderThreadState *)lpParam;
    canHandle h;
    long id;
    unsigned char data[8];
    unsigned int dlc;
    unsigned int flag;
    DWORD timestamp;
    canStatus stat;

    canInitializeLibrary();
    h = canOpenChannel(state->channel, canOPEN_ACCEPT_VIRTUAL);
    if (h < 0) {
        printf("C_ERROR: Failed to open CAN channel %d\n", state->channel);
        return 1;
    }

    stat = canSetBusParams(h, state->bitrate, 0, 0, 0, 0, 0);
    if (stat != canOK) {
        printf("C_ERROR: Failed to set bus params\n");
        canClose(h);
        return 1;
    }

    canBusOn(h);

    while (state->is_running) {
        stat = canReadWait(h, &id, &data, &dlc, &flag, &timestamp, 100); // 100ms timeout

        if (stat == canOK) {
            PyGILState_STATE gstate = PyGILState_Ensure();

            // Create a Python tuple: (arbitration_id, data_bytes, timestamp_ms)
            PyObject *py_msg = Py_BuildValue("(Ly#K)", id, data, dlc, timestamp);
            
            PyObject *result = PyObject_CallMethod(state->queue, "put_nowait", "O", py_msg);
            if (result == NULL) {
                PyErr_Print(); // Print the Python exception (e.g., queue.Full)
                fprintf(stderr, "C_WARNING: Failed to put message on Python queue.\n");
            }
            Py_XDECREF(result);
            Py_DECREF(py_msg);

            PyGILState_Release(gstate);
        } else if (stat != canERR_NOMSG) {
            char err_buf[50];
            canGetErrorText(stat, err_buf, sizeof(err_buf));
            printf("C_ERROR: canReadWait failed: %s\n", err_buf);
        }
    }

    canBusOff(h);
    canClose(h);
    printf("C_INFO: Reader thread finished.\n");
    return 0;
}

static ReaderThreadState reader_state;
static HANDLE reader_thread_handle = NULL;

static PyObject* start_reader(PyObject* self, PyObject* args) {
    int channel;
    long bitrate;
    PyObject *queue;

    if (!PyArg_ParseTuple(args, "ilO", &channel, &bitrate, &queue)) return NULL;
    
    if (!PyCallable_Check(PyObject_GetAttrString(queue, "put_nowait"))) {
        PyErr_SetString(PyExc_TypeError, "Third argument must be a queue.Queue object.");
        return NULL;
    }

    reader_state.channel = channel;
    reader_state.bitrate = bitrate;
    reader_state.queue = queue;
    Py_INCREF(reader_state.queue);
    reader_state.is_running = 1;

    reader_thread_handle = CreateThread(NULL, 0, reader_thread_func, &reader_state, 0, NULL);
    if (reader_thread_handle == NULL) {
        PyErr_SetString(PyExc_RuntimeError, "Failed to create C reader thread.");
        return NULL;
    }

    Py_RETURN_NONE;
}

static PyObject* stop_reader(PyObject* self, PyObject* args) {
    if (reader_thread_handle) {
        reader_state.is_running = 0;
        WaitForSingleObject(reader_thread_handle, 2000);
        CloseHandle(reader_thread_handle);
        reader_thread_handle = NULL;
        Py_DECREF(reader_state.queue);
    }
    Py_RETURN_NONE;
}

static PyMethodDef FastReaderMethods[] = {
    {"start", start_reader, METH_VARARGS, "Starts the CAN reader thread."},
    {"stop", stop_reader, METH_VARARGS, "Stops the CAN reader thread."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef fastreadermodule = {
    PyModuleDef_HEAD_INIT, "fast_reader", "A C extension for fast CAN bus reading.", -1, FastReaderMethods
};

PyMODINIT_FUNC PyInit_fast_reader(void) {
    return PyModule_Create(&fastreadermodule);
}