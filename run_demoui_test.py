#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = '盖华慧'


from config import setting
from package.HTMLTestRunner import HTMLTestRunner
from public.models.csvtool import CSVToolkit
from public.models.pageObjectGenerator import PageObjectGenerator
from public.models.newReport import new_report
from public.models.sendmail import send_mail
import unittest, time
import sys
import os
sys.path.append(os.path.dirname(__file__))
from pathlib import Path

# 测试报告存放文件夹，如不存在，则自动创建一个report目录
if not os.path.exists(setting.TEST_REPORT):
    os.makedirs(setting.TEST_REPORT + '/' + "screenshot")

"""将所有的testdata下的csv文件，转化为yaml文件"""
def batch_convert_csv_to_yamldata(test_path = setting.TEST_DATA_YAML):
    """
    批量将指定目录下的所有CSV文件转换为YAML格式
    Args:
        test_path: 包含CSV文件的目录路径
    """
    # 找到目录下所有CSV文件
    datapath = Path(test_path)
    print(f"处理目录: {datapath}")  # 输出: G:/DemoUI-master/testdata

    # 使用 rglob 递归查找所有 CSV 文件
    csv_files = list(datapath.rglob('*.csv'))  # 大小写敏感
    csv_files_lower = list(datapath.rglob('*.[cC][sS][vV]'))  # 大小写不敏感

    if not csv_files and not csv_files_lower:
        print(f"在目录 {datapath} 中没有找到CSV文件")
        return

    # 合并两种查找方式的结果
    all_csv_files = csv_files + csv_files_lower
    unique_csv_files = list(set(all_csv_files))  # 去重

    processed_count = 0
    error_files = []

    for csv_file in unique_csv_files:
        try:
            print(f"正在处理: {os.path.basename(csv_file)}")

            # 第一步：转换编码
            CSVToolkit.convert_encoding(csv_file, 'utf-8-sig')

            # 生成YAML文件路径（与CSV文件同名，扩展名不同）
            file_name_without_ext = os.path.splitext(csv_file)[0]
            yaml_file = f"{file_name_without_ext}.yaml"

            # 第二步：转换为YAML
            CSVToolkit.csv_to_yamldata_code(csv_file, yaml_file)

            processed_count += 1
            print(f"  ✓ 已生成: {os.path.basename(yaml_file)}")

        except Exception as e:
            error_message = f"处理 {os.path.basename(csv_file)} 失败: {str(e)}"
            print(f"  ✗ {error_message}")
            error_files.append((csv_file, str(e)))

    # 输出汇总信息
    print(f"批量转换完成！")
    print(f"成功处理: {processed_count}/{len(csv_files)} 个文件")
    if error_files:
        print(f"失败文件 ({len(error_files)} 个):")
        for file_path, error in error_files:
            print(f"  - {os.path.basename(file_path)}: {error}")
    print("\n" + "=" * 50)

"""将所有的testyaml下的csv文件，转化为yaml文件"""
def batch_convert_csv_to_yamlelement(test_path = setting.TEST_Element_YAML):
    """
    批量将指定目录下的所有CSV文件转换为YAML格式
    Args:
        test_path: 包含CSV文件的目录路径
    """
    # 找到目录下所有CSV文件
    datapath = Path(test_path)
    print(f"处理目录: {datapath}")  # 输出: G:/DemoUI-master/testyaml

    # 使用 rglob 递归查找所有 CSV 文件
    csv_files = list(datapath.rglob('*.csv'))  # 大小写敏感
    csv_files_lower = list(datapath.rglob('*.[cC][sS][vV]'))  # 大小写不敏感

    if not csv_files and not csv_files_lower:
        print(f"在目录 {datapath} 中没有找到CSV文件")
        return

    # 合并两种查找方式的结果
    all_csv_files = csv_files + csv_files_lower
    unique_csv_files = list(set(all_csv_files))  # 去重

    processed_count = 0
    error_files = []

    for csv_file in unique_csv_files:
        try:
            print(f"正在处理: {os.path.basename(csv_file)}")

            # 第一步：转换编码
            CSVToolkit.convert_encoding(csv_file, 'utf-8-sig')

            # 生成YAML文件路径（与CSV文件同名，扩展名不同）
            file_name_without_ext = os.path.splitext(csv_file)[0]
            yaml_file = f"{file_name_without_ext}.yaml"

            # 第二步：转换为YAML
            CSVToolkit.csv_to_yamlelement_code(csv_file, yaml_file)

            processed_count += 1
            print(f"  ✓ 已生成: {os.path.basename(yaml_file)}")

        except Exception as e:
            error_message = f"处理 {os.path.basename(csv_file)} 失败: {str(e)}"
            print(f"  ✗ {error_message}")
            error_files.append((csv_file, str(e)))

    # 输出汇总信息
    print(f"批量转换完成！")
    print(f"成功处理: {processed_count}/{len(csv_files)} 个文件")
    if error_files:
        print(f"失败文件 ({len(error_files)} 个):")
        for file_path, error in error_files:
            print(f"  - {os.path.basename(file_path)}: {error}")
    print("\n" + "=" * 50)

"""将所有的testyaml下的csv文件中的元素控件，转化为page的Python文件"""
def batch_generated_page(test_path = setting.TEST_Element_YAML):
    """
    批量将指定目录下的所有CSV文件转换为YAML格式
    Args:
        test_path: 包含CSV文件的目录路径
    """
    # 找到目录下所有CSV文件
    datapath = Path(test_path)
    print(f"处理目录: {datapath}")  # 输出: G:/DemoUI-master/testyaml

    # 使用 rglob 递归查找所有 CSV 文件
    csv_files = list(datapath.rglob('*.csv'))  # 大小写敏感
    csv_files_lower = list(datapath.rglob('*.[cC][sS][vV]'))  # 大小写不敏感

    if not csv_files and not csv_files_lower:
        print(f"在目录 {datapath} 中没有找到CSV文件")
        return

    # 合并两种查找方式的结果
    all_csv_files = csv_files + csv_files_lower
    unique_csv_files = list(set(all_csv_files))  # 去重

    processed_count = 0
    error_files = []

    for csv_file in unique_csv_files:
        try:
            print(f"正在处理: {os.path.basename(csv_file)}")

            # 第一步：转换编码
            CSVToolkit.convert_encoding(csv_file, 'utf-8-sig')

            # 生成YAML文件路径（与CSV文件同名，扩展名不同）
            file_name_without_ext = os.path.splitext(csv_file)[0]
            yaml_file = f"{file_name_without_ext}Page.py"
            yaml_file = yaml_file.replace("testyaml","public\\page_obj")

            # 第二步：转换为YAML
            PageObjectGenerator.csv_to_page_object(csv_file, yaml_file)

            processed_count += 1
            print(f"  ✓ 已生成: {os.path.basename(yaml_file)}")

        except Exception as e:
            error_message = f"处理 {os.path.basename(csv_file)} 失败: {str(e)}"
            print(f"  ✗ {error_message}")
            error_files.append((csv_file, str(e)))

    # 输出汇总信息
    print("\n" + "=" * 50)
    print(f"批量转换完成！")
    print(f"成功处理: {processed_count}/{len(csv_files)} 个文件")

    if error_files:
        print(f"失败文件 ({len(error_files)} 个):")
        for file_path, error in error_files:
            print(f"  - {os.path.basename(file_path)}: {error}")


"""加载所有的测试用例"""
def add_case(test_path = setting.TEST_DIR):
    discover = unittest.defaultTestLoader.discover(test_path, pattern='*_sta.py')
    return discover


"""执行所有的测试用例"""
def run_case(all_case,result_path=setting.TEST_REPORT):

    now = time.strftime("%Y-%m-%d %H_%M_%S")
    filename = result_path + '/' + now + 'result.html'
    fp = open(filename, 'wb')
    runner = HTMLTestRunner(stream=fp, title='[ICPX9437版本]UI自动化测试报告',
                            description='环境：windows 7 浏览器：chrome',
                            tester='盖华慧')
    runner.run(all_case)
    fp.close()
    report = new_report(setting.TEST_REPORT)  # 调用模块生成最新的报告
    send_mail(report)  # 调用发送邮件模块



if __name__ == "__main__":
    batch_convert_csv_to_yamldata()
    batch_convert_csv_to_yamlelement()
    batch_generated_page()
    cases = add_case()
    run_case(cases)
