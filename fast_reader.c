// fast_reader.c (with enhanced debugging)
#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <canlib.h>
#include <stdio.h>
#include <signal.h>
#include <windows.h> // For Sleep

// --- Global variables for thread management ---
static volatile int keep_running = 1;
static PyObject *py_queue = NULL;
static HANDLE reader_thread_handle = NULL;
static canHandle hnd = canINVALID_HANDLE;

// --- Helper to print Kvaser error messages ---
void print_can_error(canStatus stat, const char* function_name) {
    if (stat != canOK) {
        char err_buf[256];
        canGetErrorText(stat, err_buf, sizeof(err_buf));
        printf("C_THREAD_ERROR: %s failed. Status: %d, Message: %s\n", function_name, stat, err_buf);
        fflush(stdout);
    }
}

// --- The core function that runs in a separate thread ---
DWORD WINAPI reader_thread_func(LPVOID lpParam) {
    long id;
    unsigned char data[8];
    unsigned int dlc;
    unsigned int flag;
    DWORD time;
    canStatus stat;

    // Go on bus
    printf("C_THREAD: Attempting to go on bus...\n");
    fflush(stdout);
    stat = canBusOn(hnd);
    if (stat != canOK) {
        print_can_error(stat, "canBusOn");
        canClose(hnd);
        return 1;
    }
    printf("C_THREAD: Successfully on bus. Waiting for CAN messages...\n");
    fflush(stdout);

    // Main read loop
    while (keep_running) {
        stat = canReadWait(hnd, &id, &data, &dlc, &flag, &time, 100); // 100ms timeout

        if (stat == canOK) {
            if (py_queue != NULL) {
                PyGILState_STATE gstate = PyGILState_Ensure();

                PyObject *py_data = PyBytes_FromStringAndSize((const char*)data, dlc);
                PyObject *py_tuple = Py_BuildValue("lNO", id, py_data, PyLong_FromUnsignedLong(time));

                PyObject *put_method = PyObject_GetAttrString(py_queue, "put_nowait");
                if (put_method && PyCallable_Check(put_method)) {
                    PyObject *result = PyObject_CallFunctionObjArgs(put_method, py_tuple, NULL);
                    if (result == NULL) {
                        PyErr_Clear();
                    }
                    Py_XDECREF(result);
                }
                Py_XDECREF(put_method);
                Py_DECREF(py_tuple);

                PyGILState_Release(gstate);
            }
        } else if (stat != canERR_NOMSG) {
            print_can_error(stat, "canReadWait");
            keep_running = 0; // Stop the loop on error
        }
    }

    printf("C_THREAD: Shutting down CAN channel...\n");
    fflush(stdout);
    canBusOff(hnd);
    canClose(hnd);
    return 0;
}


// --- Python-facing function to start the thread ---
static PyObject* start_reader(PyObject* self, PyObject* args) {
    int channel;
    int bitrate;
    canStatus stat;

    printf("\n--- C EXTENSION START ---\n");
    fflush(stdout);

    if (!PyArg_ParseTuple(args, "iiO", &channel, &bitrate, &py_queue)) {
        return NULL;
    }

    if (!PyObject_HasAttrString(py_queue, "put_nowait")) {
        PyErr_SetString(PyExc_TypeError, "Argument must be a queue-like object with a 'put_nowait' method.");
        return NULL;
    }
    Py_INCREF(py_queue);

    printf("C_INIT: Initializing Kvaser CAN library...\n");
    fflush(stdout);
    canInitializeLibrary();

    printf("C_INIT: Opening Kvaser CAN channel %d...\n", channel);
    fflush(stdout);
    hnd = canOpenChannel(channel, canOPEN_ACCEPT_VIRTUAL);
    if (hnd < 0) {
        print_can_error((canStatus)hnd, "canOpenChannel");
        PyErr_SetString(PyExc_IOError, "Could not open Kvaser CAN channel.");
        return NULL;
    }
    printf("C_INIT: Channel opened successfully. Handle: %d\n", hnd);
    fflush(stdout);

    printf("C_INIT: Setting bus bitrate to %d...\n", bitrate);
    fflush(stdout);
    stat = canSetBusParams(hnd, bitrate, 0, 0, 0, 0, 0);
    if (stat != canOK) {
        print_can_error(stat, "canSetBusParams");
        canClose(hnd);
        PyErr_SetString(PyExc_IOError, "Could not set CAN bitrate.");
        return NULL;
    }
    printf("C_INIT: Bitrate set successfully.\n");
    fflush(stdout);

    printf("C_INIT: Creating reader thread...\n");
    fflush(stdout);
    keep_running = 1;
    reader_thread_handle = CreateThread(NULL, 0, reader_thread_func, NULL, 0, NULL);
    if (reader_thread_handle == NULL) {
        canClose(hnd);
        PyErr_SetString(PyExc_SystemError, "Failed to create C reader thread.");
        return NULL;
    }
    printf("C_INIT: Reader thread created successfully.\n--- C EXTENSION INITIALIZED ---\n\n");
    fflush(stdout);

    Py_RETURN_NONE;
}

// --- Python-facing function to stop the thread ---
static PyObject* stop_reader(PyObject* self, PyObject* args) {
    if (keep_running) {
        keep_running = 0;
        if (reader_thread_handle != NULL) {
            WaitForSingleObject(reader_thread_handle, 2000);
            CloseHandle(reader_thread_handle);
            reader_thread_handle = NULL;
        }
    }
    Py_XDECREF(py_queue);
    py_queue = NULL;
    Py_RETURN_NONE;
}

// --- Method definition table for the Python module ---
static PyMethodDef FastReaderMethods[] = {
    {"start", start_reader, METH_VARARGS, "Starts the CAN reader thread."},
    {"stop", stop_reader, METH_NOARGS, "Stops the CAN reader thread."},
    {NULL, NULL, 0, NULL}
};

// --- Module definition structure ---
static struct PyModuleDef fast_reader_module = {
    PyModuleDef_HEAD_INIT,
    "fast_reader",
    "A high-performance C module for reading Kvaser CAN messages.",
    -1,
    FastReaderMethods
};

// --- Module initialization function ---
PyMODINIT_FUNC PyInit_fast_reader(void) {
    return PyModule_Create(&fast_reader_module);
}