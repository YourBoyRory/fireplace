__kernel void load_gpu(__global float *data) {
    int gid = get_global_id(0);

    // Perform multiple complex operations to maximize load
    for (int i = 0; i < 10; ++i) {
        data[gid] = data[gid] * 1.0001f; // Simulate a heavy computation
        data[gid] = sin(data[gid]);      // Additional operation
        data[gid] = cos(data[gid]);      // Additional operation
    }
}

