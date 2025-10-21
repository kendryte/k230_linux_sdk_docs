# `nncase` 模型模拟器API手册

## 概述

除了编译模型 API，`nncase` 还提供了推理模型的 API，使用 `Python` 在 PC 上可推理编译模型生成的 `kmodel`，用来验证 `nncase` 推理结果和相应深度学习框架的 runtime 下生成的结果是否一致。本文档提供的 API 用于在本地 PC 上验证 `kmodel` 转换的正确性，并不是在 `k230` 上运行的代码。关于 `nncase` 的学习，请参考：[nncase github repo](https://github.com/kendryte/nncase) 。

## API 介绍

### MemoryRange

【描述】

MemoryRange类, 用于表示内存范围。

【定义】

```python
py::class_<memory_range>(m, "MemoryRange")
    .def_readwrite("location", &memory_range::memory_location)
    .def_property(
        "dtype", [](const memory_range &range) { return to_dtype(range.datatype); },
        [](memory_range &range, py::object dtype) { range.datatype = from_dtype(py::dtype::from_args(dtype)); })
    .def_readwrite("start", &memory_range::start)
    .def_readwrite("size", &memory_range::size);
```

【属性】

| 名称     | 类型           | 描述                                                                       |
| -------- | -------------- | -------------------------------------------------------------------------- |
| location | int            | 内存位置, 0表示input, 1表示output, 2表示rdata, 3表示data, 4表示shared_data |
| dtype    | python数据类型 | 数据类型                                                                   |
| start    | int            | 内存起始地址                                                               |
| Size     | int            | 内存大小                                                                   |

【示例】

`mr = nncase.MemoryRange()`

### RuntimeTensor

【描述】

RuntimeTensor类, 用于表示运行时tensor。

【定义】

```python
py::class_<runtime_tensor>(m, "RuntimeTensor")
    .def_static("from_numpy", [](py::array arr) {
        auto src_buffer = arr.request();
        auto datatype = from_dtype(arr.dtype());
        auto tensor = host_runtime_tensor::create(
            datatype,
            to_rt_shape(src_buffer.shape),
            to_rt_strides(src_buffer.itemsize, src_buffer.strides),
            gsl::make_span(reinterpret_cast<gsl::byte *>(src_buffer.ptr), src_buffer.size * src_buffer.itemsize),
            [=](gsl::byte *) { arr.dec_ref(); })
                          .unwrap_or_throw();
        arr.inc_ref();
        return tensor;
    })
    .def("copy_to", [](runtime_tensor &from, runtime_tensor &to) {
        from.copy_to(to).unwrap_or_throw();
    })
    .def("to_numpy", [](runtime_tensor &tensor) {
        auto host = tensor.as_host().unwrap_or_throw();
        auto src_map = std::move(hrt::map(host, hrt::map_read).unwrap_or_throw());
        auto src_buffer = src_map.buffer();
        return py::array(
            to_dtype(tensor.datatype()),
            tensor.shape(),
            to_py_strides(runtime::get_bytes(tensor.datatype()), tensor.strides()),
            src_buffer.data());
    })
    .def_property_readonly("dtype", [](runtime_tensor &tensor) {
        return to_dtype(tensor.datatype());
    })
    .def_property_readonly("shape", [](runtime_tensor &tensor) {
        return to_py_shape(tensor.shape());
    })
```

【属性】

| 名称  | 类型           | 描述             |
| ----- | -------------- | ---------------- |
| dtype | python数据类型 | Tensor的数据类型 |
| shape | list           | tensor的形状     |

### from_numpy

【描述】

从numpy.ndarray构造RuntimeTensor对象。

【定义】

`from_numpy(py::array arr)`

【参数】

| 名称 | 类型          | 描述              |
| ---- | ------------- | ----------------- |
| Arr  | numpy.ndarray | numpy.ndarray对象 |

【返回值】

RuntimeTensor对象。

【示例】

`tensor = nncase.RuntimeTensor.from_numpy(self.inputs[i]['data'])`

### copy_to

【描述】

拷贝RuntimeTensor。

【定义】

`copy_to(RuntimeTensor to)`

【参数】

| 名称 | 类型          | 描述              |
| ---- | ------------- | ----------------- |
| to   | RuntimeTensor | RuntimeTensor对象 |

【返回值】

无。

【示例】

`sim.get_output_tensor(i).copy_to(to)`

### to_numpy

【描述】

将RuntimeTensor转换为numpy.ndarray对象。

【定义】

`to_numpy()`

【参数】

无。

【返回值】

numpy.ndarray对象。

【示例】

`arr = sim.get_output_tensor(i).to_numpy()`

### Simulator

【描述】

Simulator类, 用于在PC上推理kmodel。

【定义】

```python
py::class_<interpreter>(m, "Simulator")
    .def(py::init())
    .def("load_model", [](interpreter &interp, gsl::span<const gsl::byte> buffer) { interp.load_model(buffer).unwrap_or_throw(); })
    .def_property_readonly("inputs_size", &interpreter::inputs_size)
    .def_property_readonly("outputs_size", &interpreter::outputs_size)
    .def("get_input_desc", &interpreter::input_desc)
    .def("get_output_desc", &interpreter::output_desc)
    .def("get_input_tensor", [](interpreter &interp, size_t index) { return interp.input_tensor(index).unwrap_or_throw(); })
    .def("set_input_tensor", [](interpreter &interp, size_t index, runtime_tensor tensor) { return interp.input_tensor(index, tensor).unwrap_or_throw(); })
    .def("get_output_tensor", [](interpreter &interp, size_t index) { return interp.output_tensor(index).unwrap_or_throw(); })
    .def("set_output_tensor", [](interpreter &interp, size_t index, runtime_tensor tensor) { return interp.output_tensor(index, tensor).unwrap_or_throw(); })
    .def("run", [](interpreter &interp) { interp.run().unwrap_or_throw(); })
```

【属性】

| 名称         | 类型 | 描述     |
| ------------ | ---- | -------- |
| inputs_size  | int  | 输入个数 |
| outputs_size | int  | 输出个数 |

【示例】

`sim = nncase.Simulator()`

### load_model

【描述】

加载kmodel。

【定义】

`load_model(model_content)`

【参数】

| 名称          | 类型     | 描述         |
| ------------- | -------- | ------------ |
| model_content | byte\[\] | kmodel字节流 |

【返回值】

无。

【示例】

`sim.load_model(kmodel)`

### get_input_desc

【描述】

获取指定索引的输入的描述信息。

【定义】

`get_input_desc(index)`

【参数】

| 名称  | 类型 | 描述       |
| ----- | ---- | ---------- |
| index | int  | 输入的索引 |

【返回值】

`MemoryRange`

【示例】

`input_desc_0 = sim.get_input_desc(0)`

### get_output_desc

【描述】

获取指定索引的输出的描述信息。

【定义】

`get_output_desc(index)`

【参数】

| 名称  | 类型 | 描述       |
| ----- | ---- | ---------- |
| index | int  | 输出的索引 |

【返回值】

`MemoryRange`

【示例】

`output_desc_0 = sim.get_output_desc(0)`

### get_input_tensor

【描述】

获取指定索引的输入的RuntimeTensor。

【定义】

`get_input_tensor(index)`

【参数】

| 名称  | 类型 | 描述             |
| ----- | ---- | ---------------- |
| index | int  | 输入tensor的索引 |

【返回值】

`RuntimeTensor`

【示例】

`input_tensor_0 = sim.get_input_tensor(0)`

### set_input_tensor

【描述】

设置指定索引的输入的RuntimeTensor。

【定义】

`set_input_tensor(index, tensor)`

【参数】

| 名称   | 类型          | 描述             |
| ------ | ------------- | ---------------- |
| index  | int           | 输入tensor的索引 |
| tensor | RuntimeTensor | 输入tensor       |

【返回值】

无。

【示例】

`sim.set_input_tensor(0, nncase.RuntimeTensor.from_numpy(self.inputs[0]['data']))`

### get_output_tensor

【描述】

获取指定索引的输出的RuntimeTensor。

【定义】

`get_output_tensor(index)`

【参数】

| 名称  | 类型 | 描述             |
| ----- | ---- | ---------------- |
| index | int  | 输出tensor的索引 |

【返回值】

`RuntimeTensor`

【示例】

`output_arr_0 = sim.get_output_tensor(0).to_numpy()`

### set_output_tensor

【描述】

设置指定索引的输出的RuntimeTensor。

【定义】

`set_output_tensor(index, tensor)`

【参数】

| 名称   | 类型          | 描述             |
| ------ | ------------- | ---------------- |
| index  | int           | 输出tensor的索引 |
| tensor | RuntimeTensor | 输出tensor       |

【返回值】

无。

【示例】

`sim.set_output_tensor(0, tensor)`

### run

【描述】

运行kmodel推理。

【定义】

`run()`

【参数】

无。

【返回值】

无。

【示例】

`sim.run()`

## 示例

假设已经对某一个onnx模型编译成kmodel模型，模拟验证脚本如下：

```python
import os
import copy
import argparse
import numpy as np
import onnx
import onnxruntime as ort
import nncase

def read_model_file(model_file):
    with open(model_file, 'rb') as f:
        model_content = f.read()
    return model_content

def cosine(gt, pred):
    return (gt @ pred) / (np.linalg.norm(gt, 2) * np.linalg.norm(pred, 2))

def main():
    parser = argparse.ArgumentParser(prog="nncase")
    parser.add_argument("--model", type=str, help='original model file')
    parser.add_argument("--model_input", type=str, help='input bin file for original model')
    parser.add_argument("--kmodel", type=str, help='kmodel file')
    parser.add_argument("--kmodel_input", type=str, help='input bin file for kmodel')
    args = parser.parse_args()

    # cpu inference
    ort_session = ort.InferenceSession(args.model)
    output_names = []
    model_outputs = ort_session.get_outputs()
    for i in range(len(model_outputs)):
        output_names.append(model_outputs[i].name)
    model_input = ort_session.get_inputs()[0]
    model_input_name = model_input.name
    model_input_type = np.float32
    model_input_shape = model_input.shape
    model_input_data = np.fromfile(args.model_input, model_input_type).reshape(model_input_shape)
    cpu_results = []
    cpu_results = ort_session.run(output_names, { model_input_name : model_input_data })

    # create simulator
    sim = nncase.Simulator()

    # read kmodel
    kmodel = read_model_file(args.kmodel)

    # load kmodel
    sim.load_model(kmodel)

    # read input.bin
    # input_tensor=sim.get_input_tensor(0).to_numpy()
    dtype = sim.get_input_desc(0).dtype
    input = np.fromfile(args.kmodel_input, dtype).reshape([1, 3, 320, 320])

    # set input for simulator
    sim.set_input_tensor(0, nncase.RuntimeTensor.from_numpy(input))

    # simulator inference
    nncase_results = []
    sim.run()
    for i in range(sim.outputs_size):
        nncase_result = sim.get_output_tensor(i).to_numpy()
        nncase_results.append(copy.deepcopy(nncase_result))

    # compare
    for i in range(sim.outputs_size):
        cos = cosine(np.reshape(nncase_results[i], (-1)), np.reshape(cpu_results[i], (-1)))
        print('output {0} cosine similarity : {1}'.format(i, cos))

if __name__ == '__main__':
    main()
```

使用保存的bin文件中的输入数据，对onnx和kmodel的推理结果计算cosine相似度，可以得到模型转换的正确性。
