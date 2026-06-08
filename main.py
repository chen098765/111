import os
import argparse
from modules.document_reader import DocumentReader
from modules.comparator import ReportComparator
from modules.scorer import ReportScorer
from modules.report_generator import ReportGenerator

def grade_report(student_file, reference_file, output_format='html', config_file='config/scoring_rules.json'):
    """批改单个报告"""
    reader = DocumentReader()
    comparator = ReportComparator()
    scorer = ReportScorer(config_file)
    generator = ReportGenerator('output')
    
    print(f"正在读取参考答案: {reference_file}")
    reference_report = reader.read_document(reference_file)
    
    print(f"正在读取学生报告: {student_file}")
    student_report = reader.read_document(student_file)
    
    print("正在比对报告内容...")
    comparison_result = comparator.compare_reports(student_report, reference_report)
    
    print("正在评分...")
    scoring_result = scorer.score_report(comparison_result)
    
    print("正在生成评语...")
    feedback = scorer.generate_feedback(comparison_result, scoring_result)
    
    print(f"正在生成{output_format.upper()}报告...")
    output_path = generator.generate_report(
        student_file, reference_file, 
        comparison_result, scoring_result, 
        feedback, output_format
    )
    
    print(f"批改完成！报告已保存至: {output_path}")
    print(f"总分: {scoring_result['total']}/100")
    
    return {
        'output_path': output_path,
        'total_score': scoring_result['total'],
        'feedback': feedback
    }

def batch_grade(student_folder, reference_file, output_format='html', config_file='config/scoring_rules.json'):
    """批量批改文件夹中的报告"""
    results = []
    
    for filename in os.listdir(student_folder):
        filepath = os.path.join(student_folder, filename)
        if os.path.isfile(filepath):
            _, ext = os.path.splitext(filename)
            if ext.lower() in ['.docx', '.pdf']:
                print(f"\n处理文件: {filename}")
                try:
                    result = grade_report(filepath, reference_file, output_format, config_file)
                    results.append({
                        'filename': filename,
                        'score': result['total_score'],
                        'output_path': result['output_path']
                    })
                except Exception as e:
                    print(f"处理 {filename} 时出错: {str(e)}")
                    results.append({
                        'filename': filename,
                        'score': None,
                        'error': str(e)
                    })
    
    print("\n=== 批量处理完成 ===")
    for result in results:
        if result['score'] is not None:
            print(f"{result['filename']}: {result['score']}/100 -> {result['output_path']}")
        else:
            print(f"{result['filename']}: 处理失败 - {result['error']}")
    
    return results

def main():
    parser = argparse.ArgumentParser(description='实训报告自动批改系统')
    parser.add_argument('--reference', '-r', required=True, help='参考答案文件路径')
    parser.add_argument('--student', '-s', help='学生报告文件路径')
    parser.add_argument('--folder', '-f', help='学生报告文件夹路径（批量处理）')
    parser.add_argument('--format', '-o', choices=['html', 'json'], default='html', help='输出格式')
    parser.add_argument('--config', '-c', default='config/scoring_rules.json', help='评分配置文件路径')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.reference):
        print(f"错误：参考答案文件不存在: {args.reference}")
        return
    
    if args.student:
        if not os.path.exists(args.student):
            print(f"错误：学生报告文件不存在: {args.student}")
            return
        grade_report(args.student, args.reference, args.format, args.config)
    elif args.folder:
        if not os.path.isdir(args.folder):
            print(f"错误：文件夹不存在: {args.folder}")
            return
        batch_grade(args.folder, args.reference, args.format, args.config)
    else:
        print("错误：请指定学生报告文件(--student)或文件夹(--folder)")
        parser.print_help()

if __name__ == '__main__':
    main()