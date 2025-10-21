# `nncase` 模型编译 API 手册

## 概述

`nncase` 是一个为 AI 加速器设计的神经网络编译器。本文档给出的 API 是用户使用的`python API`,用于将训练好的 `TFLite` 模型或 `ONNX` 模型转换成能够使用 `kpu` 加速的模型格式，即 `kmodel`。目前编译模型 APIs 支持 `TFLite/ONNX` 等格式的深度学习模型。本文档提供的 API 用于在本地 PC 上编译出 `kmodel` ，并不是在 `k230` 上运行的代码。关于 `nncase` 的学习，请参考：[nncase github repo](https://github.com/kendryte/nncase) 。

## API 介绍

### CompileOptions

【描述】

CompileOptions类, 用于配置nncase编译选项，各属性说明如下：

| 属性名称                    |         类型          | 是否必须 | 描述                                                                                                                   |
| :-------------------------- | :-------------------: | :------: | ---------------------------------------------------------------------------------------------------------------------- |
| target                      |        string         |    是    | 指定编译目标, 如'cpu', 'k230'                                                                                          |
| dump_ir                     |         bool          |    否    | 指定是否dump IR, 默认为False                                                                                           |
| dump_asm                    |         bool          |    否    | 指定是否dump asm汇编文件, 默认为False                                                                                  |
| dump_dir                    |        string         |    否    | 前面指定dump_ir等开关后, 这里指定dump的目录, 默认为""                                                                  |
| input_file                  |        string         |    否    | ONNX模型超过2GB时，用于指定参数文件路径，默认为""                                                                      |
| preprocess                  |         bool          |    否    | 是否开启前处理，默认为False。以下参数仅在 `preprocess=True`时生效                                                      |
| input_type                  |        string         |    否    | 开启前处理时指定输入数据类型，默认为"float"。当 `preprocess`为 `True`时，必须指定为"uint8"或者"float32"                |
| input_shape                 |       list[int]       |    否    | 开启前处理时指定输入数据的shape，默认为[]。当 `preprocess`为 `True`时，必须指定                                        |
| input_range                 |      list[float]      |    否    | 开启前处理时指定输入数据反量化后的浮点数范围，默认为[ ]。当 `preprocess`为 `True`且 `input_type`为 `uint8`时，必须指定 |
| input_layout                |        string         |    否    | 指定输入数据的layout，默认为""                                                                                         |
| swapRB                      |         bool          |    否    | 是否在 `channel`维度反转数据，默认为False                                                                              |
| mean                        |      list[float]      |    否    | 前处理标准化参数均值，默认为[0,0,0]                                                                                    |
| std                         |      list[float]      |    否    | 前处理标准化参数方差，默认为[1,1,1]                                                                                    |
| letterbox_value             |         float         |    否    | 指定前处理letterbox的填充值，默认为0                                                                                   |
| output_layout               |        string         |    否    | 指定输出数据的layout, 默认为""                                                                                         |
| shape_bucket_enable         |         bool          |    是    | 是否开启ShapeBucket功能，默认为False。在 `dump_ir=True`时生效                                                          |
| shape_bucket_range_info     | Dict[str, [int, int]] |    是    | 每个输入shape维度信息中的变量的范围，最小值必须大于等于1                                                               |
| shape_bucket_segments_count |          int          |    是    | 输入变量的范围划分为几段                                                                                               |
| shape_bucket_fix_var_map    |    Dict[str, int]     |    否    | 固定shape维度信息中的变量为特定的值                                                                                    |

#### 前处理流程说明

目前暂不支持自定义前处理顺序，可以根据以下流程示意图，选择所需要的前处理参数进行配置。

<div class="mermaid">
graph TD;
    NewInput("NewInput<br>(shape = input_shape<br>dtype = input_type)") -->a(input_layout != ' ')-.Y.->Transpose1["transpose"] -.->b("SwapRB == True")-.Y.->SwapRB["SwapRB"]-.->c("input_type != float32")-.Y.->Dequantize["Dequantize"]-.->d("input_HW != model_HW")-.Y.->LetterBox["LetterBox"] -.->e("std not empty<br>mean not empty")-.Y.->Normalization["Normalization"]-.->OldInput-->Model_body-->OldOutput-->f("output_layout != ' '")-.Y.->Transpose2["Transpose"]-.-> NewOutput;
    a--N-->b--N-->c--N-->d--N-->e--N-->OldInput; f--N-->NewOutput;
    subgraph origin_model
        OldInput; Model_body ; OldOutput;
    end
</div>

参数说明：

1. `input_range`为输入数据类型为定点时，反量化后的浮点数范围。

   a. 输入数据类型为uint8，range为[0,255]，`input_range`为[0,255]，则反量化的作用只是进行类型转化，将uint8的数据转化为float32，`mean`和 `std`参数仍然按照[0,255]的数据进行指定。

   b. 输入数据类型为uint8，range为[0,255]，`input_range`为[0,1]，则反量化会将定点数转化为浮点数[0,1]，`mean`和 `std`参数需要按照0~1的数据进行指定。

   <div class="mermaid">
    graph TD;
        NewInput_uint8("NewInput_uint8 <br>[input_type:uint8]") --input_range:0,255 -->dequantize_0["Dequantize"]--float range:0,255--> OldInput_float32
        NewInput_uint81("NewInput_uint8 <br>[input_type:uint8]") --input_range:0,1 -->dequantize_1["Dequantize"]--float range:0,1--> OldInput_float32
   </div>

1. `input_shape`为输入数据的shape，layout为 `input_layout`，现在支持字符串（`"NHWC"`、`"NCHW"`）和index两种方式作为 `input_layout`，并且支持非4D的数据处理。
当按照字符串形式配置 `input_layout`时，表示输入数据的layout；当按照index形式配置`input_layout`时，表示输入数据会按照当前配置的 `input_layout`进行数据转置，即 `input_layout`为 `Transpose`的 `perm`参数。

<div class="mermaid">
graph TD;
    subgraph B
        NewInput1("NewInput: 1,4,10") --"input_layout:"0,2,1""-->Transpose2("Transpose perm: 0,2,1") --> OldInput2("OldInput: 1,10,4");
    end
    subgraph A
        NewInput --"input_layout:"NHWC""--> Transpose0("Transpose: NHWC2NCHW") --> OldInput;
        NewInput("NewInput: 1,224,224,3 (NHWC)") --"input_layout:"0,3,1,2""--> Transpose1("Transpose perm: 0,3,1,2") --> OldInput("OldInput: 1,3,224,224 (NCHW)");
    end
</div>

​   `output_layout`同理，如下图所示。

<div class="mermaid">
graph TD;
subgraph B
    OldOutput1("OldOutput: 1,10,4,5,2") --"output_layout: "0,2,3,1,4""--> Transpose5("Transpose perm: 0,2,3,1,4") --> NewOutput1("NewOutput: 1,4,5,10,2");
    end
subgraph A
    OldOutput --"output_layout: "NHWC""--> Transpose3("Transpose: NCHW2NHWC") --> NewOutput("NewOutput<br>NHWC");
    OldOutput("OldOutput: (NCHW)") --"output_layout: "0,2,3,1""--> Transpose4("Transpose perm: 0,2,3,1") --> NewOutput("NewOutput<br>NHWC");
    end
</div>

#### 动态shape参数说明

ShapeBucket是针对动态shape的一种解决方案，会根据输入长度的范围以及指定的段的数量来对动态shape进行优化。该功能默认为false，需要打开对应的option才能生效，除了指定对应的字段信息，其他流程与编译静态模型没有区别。

- ONNX

在模型的shape中会有些维度为变量名字，这里以一个ONNX模型的输入为例。

> tokens: int64[batch_size, tgt_seq_len]
> step: float32[seq_len, batch_size]

shape的维度信息中存在`seq_len`，`tgt_seq_len`，`batch_size`这三个变量。
首先是batch_size，虽然是变量的但实际应用的时候固定为3，因此在**fix_var_map**中添加`batch_size = 3`，在运行的时候会将这个维度固定为3。
`seq_len`，`tgt_seq_len`两个是实际会发生改变的，因此需要配置这两个变量的实际范围，也就是**range_info**的信息。**segments_count**是实际分段的数量，会根据范围等分为几份，对应的编译时间也会相应增加几倍。

以下为对应的编译参数示例：

```python
compile_options = nncase.CompileOptions()
compile_options.shape_bucket_enable = True
compile_options.shape_bucket_range_info = {"seq_len": [1, 100], "tgt_seq_len": [1, 100]}
compile_options.shape_bucket_segments_count = 2
compile_options.shape_bucket_fix_var_map = {"batch_size": 3}
```

- TFLite

TFLite的模型与ONNX不同，shape上暂未标注维度的名称，目前只支持输入中具有一个维度是动态的，并且名称统一配置为-1，配置方式如下：

```cpp
compile_options = nncase.CompileOptions()
compile_options.shape_bucket_enable = True
compile_options.shape_bucket_range_info = {"-1":[1, 100]}
compile_options.shape_bucket_segments_count = 2
compile_options.shape_bucket_fix_var_map = {"batch_size" : 3}
```

配置完这些选项后整个编译的流程和静态shape一致。

#### 参数配置示例

实例化CompileOptions，配置各属性的值。

```python
compile_options = nncase.CompileOptions()

compile_options.target = "cpu" #"k230"
compile_options.dump_ir = True  # if False, will not dump the compile-time result.
compile_options.dump_asm = True
compile_options.dump_dir = "dump_path"
compile_options.input_file = ""

# preprocess args
compile_options.preprocess = False
if compile_options.preprocess:
    compile_options.input_type = "uint8"  # "uint8" "float32"
    compile_options.input_shape = [1,224,320,3]
    compile_options.input_range = [0,1]
    compile_options.input_layout = "NHWC" # "NHWC" ”NCHW“
    compile_options.swapRB = False
    compile_options.mean = [0,0,0]
    compile_options.std = [1,1,1]
    compile_options.letterbox_value = 0
    compile_options.output_layout = "NHWC" # "NHWC" "NCHW"

# Dynamic shape args
compile_options.shape_bucket_enable = False
if compile_options.shape_bucket_enable:
    compile_options.shape_bucket_range_info = {"seq_len": [1, 100], "tgt_seq_len": [1, 100]}
    compile_options.shape_bucket_segments_count = 2
    compile_options.shape_bucket_fix_var_map = {"batch_size": 3}
```

### ImportOptions

【描述】

ImportOptions类, 用于配置nncase导入选项。

【定义】

```python
class ImportOptions:
    def __init__(self) -> None:
        pass
```

【示例】

实例化ImportOptions, 配置各属性的值。

```python
#import_options
import_options = nncase.ImportOptions()
```

### PTQTensorOptions

【描述】

PTQTensorOptions类, 用于配置nncase PTQ选项。

| 名称                           | 类型   | 是否必须 | 描述 |
| ------------------------------ | ------ | -------- | ---- |
| samples_count                  | int    |    否    |  指定用于量化的校正集数量    |
| calibrate_method               | string |    否    |  指定量化方法，可选'NoClip'、'Kld'，默认为'Kld'   |
| finetune_weights_method        | string |    否    |  指定是否对权重进行微调，可选'NoFineTuneWeights'、'UseSquant'，默认为'NoFineTuneWeights'  |
| quant_type                     | string |    否    |  指定数据量化类型，可选'uint8'，'int8'，'int16'，`quant_type`和`w_quant_type`两种类型不可同时为'int16'  |
| w_quant_type                   | string |    否    |  指定权重量化类型，可选'uint8'，'int8'，'int16'，`quant_type`和`w_quant_type`两种类型不可同时为'int16' |
| quant_scheme                   | string |    否    |  导入量化参数配置文件的路径 |
| quant_scheme_strict_mode       | bool   |    否    |  是否严格按照quant_scheme执行量化  |
| export_quant_scheme            | bool   |    否    |  是否导出量化参数配置文件  |
| export_weight_range_by_channel | bool   |    否    |  是否导出 `bychannel`形式的weights量化参数，该参数建议设置为 `True`  |

混合量化具体使用流程见 [MixQuant说明](https://github.com/kendryte/nncase/blob/release/2.0/docs/MixQuant.md)。

【示例】

```python
# ptq_options
ptq_options = nncase.PTQTensorOptions()
ptq_options.samples_count = 6
ptq_options.finetune_weights_method = "NoFineTuneWeights"
ptq_options.quant_type = "uint8"
ptq_options.w_quant_type = "uint8"
ptq_options.set_tensor_data(generate_data(input_shape, ptq_options.samples_count, args.dataset))

ptq_options.quant_scheme = ""
ptq_options.quant_scheme_strict_mode = False
ptq_options.export_quant_scheme = True
ptq_options.export_weight_range_by_channel = True

compiler.use_ptq(ptq_options)
```

### set_tensor_data

【描述】

设置tensor数据，设置模型转换过程中的校准数据。

【定义】

```python
    def set_tensor_data(self, data: List[List[np.ndarray]]) -> None:
        reshape_data = list(map(list, zip(*data)))
        self.cali_data = [RuntimeTensor.from_numpy(
            d) for d in itertools.chain.from_iterable(reshape_data)]
```

【参数】

| 名称 | 类型                  | 描述           |
| ---- | --------------------- | -------------- |
| data | List[List[np.ndarray]] | 读取的校准数据 |

【返回值】

无。

【示例】

```shell
# ptq_options
ptq_options = nncase.PTQTensorOptions()
ptq_options.samples_count = 6
ptq_options.set_tensor_data(generate_data(input_shape, ptq_options.samples_count, args.dataset))
compiler.use_ptq(ptq_options)
```

### Compiler

【描述】

Compiler类, 用于编译神经网络模型。

【定义】

```python
class Compiler:
    _target: _nncase.Target
    _session: _nncase.CompileSession
    _compiler: _nncase.Compiler
    _compile_options: _nncase.CompileOptions
    _quantize_options: _nncase.QuantizeOptions
    _module: IRModule
```

### import_tflite

【描述】

导入TFLite模型。

【定义】

```python
def import_tflite(self, model_content: bytes, options: ImportOptions) -> None:
    self._compile_options.input_format = "tflite"
    self._import_module(model_content)
```

【参数】

| 名称           | 类型          | 描述           |
| -------------- | ------------- | -------------- |
| model_content  | byte\[\]      | 读取的模型内容 |
| import_options | ImportOptions | 导入选项       |

【返回值】

无。

【示例】

```python
model_content = read_model_file(model)
compiler.import_tflite(model_content, import_options)
```

### import_onnx

【描述】

导入ONNX模型。

【定义】

```python
def import_onnx(self, model_content: bytes, options: ImportOptions) -> None:
    self._compile_options.input_format = "onnx"
    self._import_module(model_content)
```

【参数】

| 名称           | 类型          | 描述           |
| -------------- | ------------- | -------------- |
| model_content  | byte\[\]      | 读取的模型内容 |
| import_options | ImportOptions | 导入选项       |

【返回值】

无。

【示例】

```python
model_content = read_model_file(model)
compiler.import_onnx(model_content, import_options)
```

### use_ptq

【描述】

设置PTQ配置选项。

- K230默认必须使用量化。

【定义】

`use_ptq(ptq_options)`

【参数】

| 名称        | 类型             | 描述        |
| ----------- | ---------------- | ----------- |
| ptq_options | PTQTensorOptions | PTQ配置选项 |

【返回值】

无。

【示例】

`compiler.use_ptq(ptq_options)`

### compile

【描述】

编译神经网络模型。

【定义】

`compile()`

【参数】

无。

【返回值】

无。

【示例】

`compiler.compile()`

### gencode_tobytes

【描述】

生成kmodel字节流。

【定义】

`gencode_tobytes()`

【参数】

无。

【返回值】

`bytes[]`

【示例】

```python
kmodel = compiler.gencode_tobytes()
with open(os.path.join(infer_dir, 'test.kmodel'), 'wb') as f:
    f.write(kmodel)
```

## 示例

### 编译TFLite模型

示例编译脚本如下：

```python
import os
import argparse
import numpy as np
from PIL import Image
import nncase

def read_model_file(model_file):
    with open(model_file, 'rb') as f:
        model_content = f.read()
    return model_content

def generate_data(shape, batch, calib_dir):
    img_paths = [os.path.join(calib_dir, p) for p in os.listdir(calib_dir)]
    data = []
    for i in range(batch):
        assert i < len(img_paths), "calibration images not enough."
        img_data = Image.open(img_paths[i]).convert('RGB')
        img_data = img_data.resize((shape[3], shape[2]), Image.BILINEAR)
        img_data = np.asarray(img_data, dtype=np.uint8)
        img_data = np.transpose(img_data, (2, 0, 1))
        data.append([img_data[np.newaxis, ...]])
    return data

def main():
    parser = argparse.ArgumentParser(prog="nncase")
    parser.add_argument("--target", type=str, help='target to run')
    parser.add_argument("--model", type=str, help='model file')
    parser.add_argument("--dataset", type=str, help='calibration_dataset')
    args = parser.parse_args()

    input_shape = [1, 3, 224, 224]
    dump_dir = 'tmp/mbv2_tflite'

    # compile_options
    compile_options = nncase.CompileOptions()
    compile_options.target = args.target
    compile_options.preprocess = True
    compile_options.swapRB = False
    compile_options.input_shape = input_shape
    compile_options.input_type = 'uint8'
    compile_options.input_range = [0, 255]
    compile_options.mean = [127.5, 127.5, 127.5]
    compile_options.std = [127.5, 127.5, 127.5]
    compile_options.input_layout = 'NCHW'
    compile_options.dump_ir = True
    compile_options.dump_asm = True
    compile_options.dump_dir = dump_dir

    # compiler
    compiler = nncase.Compiler(compile_options)

    # import
    model_content = read_model_file(args.model)
    import_options = nncase.ImportOptions()
    compiler.import_tflite(model_content, import_options)

    # ptq_options
    ptq_options = nncase.PTQTensorOptions()
    ptq_options.samples_count = 6
    ptq_options.set_tensor_data(generate_data(input_shape, ptq_options.samples_count, args.dataset))
    compiler.use_ptq(ptq_options)

    # compile
    compiler.compile()

    # kmodel
    kmodel = compiler.gencode_tobytes()
    with open(os.path.join(dump_dir, 'test.kmodel'), 'wb') as f:
        f.write(kmodel)

if __name__ == '__main__':
    main()
```

执行如下命令即可编译指定的TFLite模型为kmodel, target为k230。

### 编译ONNX模型

针对ONNX模型, 建议先使用[ONNX Simplifier](https://github.com/daquexian/onnx-simplifier)进行简化, 然后再使用nncase编译。

示例编译脚本如下：

```python
import os
import argparse
import numpy as np
from PIL import Image
import onnxsim
import onnx
import nncase

def parse_model_input_output(model_file):
    onnx_model = onnx.load(model_file)
    input_all = [node.name for node in onnx_model.graph.input]
    input_initializer = [node.name for node in onnx_model.graph.initializer]
    input_names = list(set(input_all) - set(input_initializer))
    input_tensors = [
        node for node in onnx_model.graph.input if node.name in input_names]

    # input
    inputs = []
    for _, e in enumerate(input_tensors):
        onnx_type = e.type.tensor_type
        input_dict = {}
        input_dict['name'] = e.name
        input_dict['dtype'] = onnx.mapping.TENSOR_TYPE_TO_NP_TYPE[onnx_type.elem_type]
        input_dict['shape'] = [(i.dim_value if i.dim_value != 0 else d) for i, d in zip(
            onnx_type.shape.dim, [1, 3, 224, 224])]
        inputs.append(input_dict)

    return onnx_model, inputs


def onnx_simplify(model_file, dump_dir):
    onnx_model, inputs = parse_model_input_output(model_file)
    onnx_model = onnx.shape_inference.infer_shapes(onnx_model)
    input_shapes = {}
    for input in inputs:
        input_shapes[input['name']] = input['shape']

    onnx_model, check = onnxsim.simplify(onnx_model, input_shapes=input_shapes)
    assert check, "Simplified ONNX model could not be validated"

    model_file = os.path.join(dump_dir, 'simplified.onnx')
    onnx.save_model(onnx_model, model_file)
    return model_file


def read_model_file(model_file):
    with open(model_file, 'rb') as f:
        model_content = f.read()
    return model_content

def generate_data_ramdom(shape, batch):
    data = []
    for i in range(batch):
        data.append([np.random.randint(0, 256, shape).astype(np.uint8)])
    return data


def generate_data(shape, batch, calib_dir):
    img_paths = [os.path.join(calib_dir, p) for p in os.listdir(calib_dir)]
    data = []
    for i in range(batch):
        assert i < len(img_paths), "calibration images not enough."
        img_data = Image.open(img_paths[i]).convert('RGB')
        img_data = img_data.resize((shape[3], shape[2]), Image.BILINEAR)
        img_data = np.asarray(img_data, dtype=np.uint8)
        img_data = np.transpose(img_data, (2, 0, 1))
        data.append([img_data[np.newaxis, ...]])
    return data

def main():
    parser = argparse.ArgumentParser(prog="nncase")
    parser.add_argument("--target", type=str, help='target to run')
    parser.add_argument("--model", type=str, help='model file')
    parser.add_argument("--dataset", type=str, help='calibration_dataset')

    args = parser.parse_args()

    input_shape = [1, 3, 320, 320]

    dump_dir = 'tmp/yolov5s_onnx'
    if not os.path.exists(dump_dir):
        os.makedirs(dump_dir)

    # onnx simplify
    model_file = onnx_simplify(args.model, dump_dir)

    # compile_options
    compile_options = nncase.CompileOptions()
    compile_options.target = args.target
    compile_options.preprocess = True
    compile_options.swapRB = False
    compile_options.input_shape = input_shape
    compile_options.input_type = 'uint8'
    compile_options.input_range = [0, 255]
    compile_options.mean = [0, 0, 0]
    compile_options.std = [255, 255, 255]
    compile_options.input_layout = 'NCHW'
    compile_options.output_layout = 'NCHW'
    compile_options.dump_ir = True
    compile_options.dump_asm = True
    compile_options.dump_dir = dump_dir

    # compiler
    compiler = nncase.Compiler(compile_options)

    # import
    model_content = read_model_file(model_file)
    import_options = nncase.ImportOptions()
    compiler.import_onnx(model_content, import_options)

    # ptq_options
    ptq_options = nncase.PTQTensorOptions()
    ptq_options.samples_count = 6
    ptq_options.set_tensor_data(generate_data(input_shape, ptq_options.samples_count, args.dataset))
    compiler.use_ptq(ptq_options)

    # compile
    compiler.compile()

    # kmodel
    kmodel = compiler.gencode_tobytes()
    with open(os.path.join(dump_dir, 'test.kmodel'), 'wb') as f:
        f.write(kmodel)

if __name__ == '__main__':
    main()
```

执行如下命令即可编译指定的ONNX模型为kmodel, target为k230。
