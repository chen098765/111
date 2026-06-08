import streamlit as st
import os
import tempfile
from modules.document_reader import DocumentReader
from modules.comparator import ReportComparator
from modules.scorer import ReportScorer
from modules.report_generator import ReportGenerator

def main():
    st.set_page_config(page_title="实训报告自动批改系统", layout="wide")
    
    st.title("📝 实训报告自动批改系统")
    
    st.sidebar.header("系统设置")
    output_format = st.sidebar.selectbox("输出格式", ["HTML", "JSON"], index=0)
    show_feedback = st.sidebar.checkbox("显示评语", value=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📎 上传参考答案")
        reference_file = st.file_uploader("选择参考答案文件 (.docx 或 .pdf)", type=["docx", "pdf"])
    
    with col2:
        st.subheader("📎 上传学生报告")
        student_files = st.file_uploader(
            "选择学生报告文件 (.docx 或 .pdf)", 
            type=["docx", "pdf"],
            accept_multiple_files=True
        )
    
    if st.button("🚀 开始批改", disabled=not (reference_file and student_files)):
        with tempfile.TemporaryDirectory() as tmp_dir:
            ref_path = os.path.join(tmp_dir, reference_file.name)
            with open(ref_path, 'wb') as f:
                f.write(reference_file.getvalue())
            
            reader = DocumentReader()
            comparator = ReportComparator()
            scorer = ReportScorer('config/scoring_rules.json')
            generator = ReportGenerator('output')
            
            st.subheader("📊 批改结果")
            
            results = []
            for student_file in student_files:
                try:
                    stu_path = os.path.join(tmp_dir, student_file.name)
                    with open(stu_path, 'wb') as f:
                        f.write(student_file.getvalue())
                    
                    reference_report = reader.read_document(ref_path)
                    student_report = reader.read_document(stu_path)
                    
                    comparison_result = comparator.compare_reports(student_report, reference_report)
                    scoring_result = scorer.score_report(comparison_result)
                    feedback = scorer.generate_feedback(comparison_result, scoring_result)
                    
                    output_path = generator.generate_report(
                        stu_path, ref_path, 
                        comparison_result, scoring_result, 
                        feedback, output_format.lower()
                    )
                    
                    results.append({
                        'filename': student_file.name,
                        'score': scoring_result['total'],
                        'scores': scoring_result['scores'],
                        'feedback': feedback,
                        'output_path': output_path,
                        'comparison': comparison_result
                    })
                except Exception as e:
                    st.error(f"处理 {student_file.name} 时出错: {str(e)}")
            
            for result in results:
                with st.expander(f"📄 {result['filename']}"):
                    st.metric("总分", f"{result['score']}/100")
                    
                    col_a, col_b, col_c = st.columns(3)
                    col_a.metric("结构完整性", f"{result['scores']['structure']:.1f}/10")
                    col_b.metric("步骤准确性", f"{result['scores']['accuracy']:.1f}/30")
                    col_c.metric("结果匹配度", f"{result['scores']['matching']:.1f}/25")
                    
                    col_d, col_e, col_f = st.columns(3)
                    col_d.metric("分析深度", f"{result['scores']['analysis']:.1f}/20")
                    col_e.metric("图片质量", f"{result['scores']['images']:.1f}/10")
                    col_f.metric("格式规范", f"{result['scores']['format']:.1f}/5")
                    
                    if show_feedback:
                        st.subheader("💬 评语")
                        st.write(result['feedback'])
                    
                    with open(result['output_path'], 'r', encoding='utf-8') as f:
                        report_content = f.read()
                    
                    download_button = st.download_button(
                        label=f"📥 下载批改报告",
                        data=report_content,
                        file_name=os.path.basename(result['output_path']),
                        mime="text/html" if output_format == "HTML" else "application/json"
                    )

if __name__ == '__main__':
    main()