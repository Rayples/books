import os
import fitz  # PyMuPDF库导入时使用的名称是fitz

def split_pdf_with_bookmarks(input_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    doc = fitz.open(input_path)
    total_pages = doc.page_count
    bookmarks = doc.get_toc()  # 获取原PDF的书签信息

    for start_page in range(0, total_pages, 100):
        end_page = min(start_page + 100, total_pages)
        new_doc = fitz.open()  # 创建新的PDF文档对象

        # 复制页面到新文档
        for page_num in range(start_page, end_page):
            new_doc.insert_page(-1, doc[page_num])

        output_file_name = os.path.join(output_folder, f'电子工程师自学速成 入门篇 超清书签版_{start_page // 100 + 1}.pdf')

        # 处理书签，使其对应新文档中的页面
        new_bookmarks = []
        for bookmark in bookmarks:
            level, title, page_dest = bookmark
            if page_dest >= start_page and page_dest < end_page:
                new_page_dest = page_dest - start_page
                new_bookmark = (level, title, new_page_dest)
                new_bookmarks.append(new_bookmark)

        new_doc.set_toc(new_bookmarks)  # 设置新文档的书签

        new_doc.save(output_file_name)  # 保存新的PDF文件

input_pdf_path = '电子工程师自学速成 入门篇 超清书签版.pdf'  # 替换成实际的PDF文件路径
output_folder_path = 'split_pdfs'  # 可以自行设置输出文件夹名称
split_pdf_with_bookmarks(input_pdf_path, output_folder_path)