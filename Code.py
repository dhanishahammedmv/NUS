import fitz


def find_page_number_of_text(text_path, pdf_path, output_path):
    with open(text_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    pdf_given = fitz.open(pdf_path)

    paragraph_num = 1
    inside_paragraph = True
    paragraphs_with_page_numbers = []
    current_paragraph = []

    for line in lines:
        if f'paragraph_{paragraph_num}' in line.lower():
            inside_paragraph = True
            current_paragraph = []
        elif inside_paragraph and line.strip():
            current_paragraph.append(line.strip())
        elif inside_paragraph and not line.strip():
            inside_paragraph = False
            page_num = find_page_numbers_for_paragraph(pdf_given, current_paragraph)
            paragraphs_with_page_numbers.append((current_paragraph, page_num))
            paragraph_num += 1
    if current_paragraph:
        page_num = find_page_numbers_for_paragraph(pdf_given, current_paragraph)
        paragraphs_with_page_numbers.append((current_paragraph, page_num))

    with open(output_path, 'w', encoding='utf-8') as output:
        for x, (paragraph, page_num) in enumerate(paragraphs_with_page_numbers, start=1):
            page_numbers_str = ', '.join(map(str, page_num))
            output.write(f"Page Numbers for paragraph_{x}: {page_numbers_str}\n")

    pdf_given.close()


def find_page_numbers_for_paragraph(pdf_given, paragraph):
    page_num = set()
    for term in paragraph:
        page_num.update(find_page_numbers_for_term(pdf_given, term))
    return sorted(list(page_num))


def find_page_numbers_for_term(pdf_given, term):
    page_num = set()
    for page_no in range(pdf_given.page_count):
        page = pdf_given[page_no]
        if term.strip().lower() in page.get_text("text").lower().strip():
            page_num.add(page_no + 1)
    return sorted(list(page_num))


find_page_number_of_text('text_file.txt', 'pdf_file.pdf', 'output.txt')