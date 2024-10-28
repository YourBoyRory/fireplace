__kernel void load_gpu(__global float *data) {
    int gid = get_global_id(0);

    // change i < 10 to pound the GPU harder, higer is more lower is less
    // 10 heats the GPU up but still makes the system usable hopfully
    for (int i = 0; i < 10; ++i) {
        data[gid] = data[gid] * 1.0001f;
        data[gid] = sin(data[gid]);
        data[gid] = cos(data[gid]);
    }
}

