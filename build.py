import json

index_template_file="template/index.html"
paper_data="data/papers"

def generate_main(index_content, paper_list, student_list):
    if paper_list!=None:
        index_content = index_content.replace("<!--PAPER-LIST-->", paper_list)
    if student_list!=None:
        index_content = index_content.replace("<!--STUDENT-LIST-->", student_list)
    write_file("index.html", index_content)

def read_file(filename):
    with open(filename, 'r') as file:
        file_content = file.read()
        return file_content

def write_file(filename, content):
    with open(filename, 'w') as file:
        file.write(content)

def build_paper(title, author, conference, year, pdf, tool, video, ppt, award):
    paper_content = "          <li>\n \
           <h4 class=""><strong>TITLE</strong>\n"
    paper_content = paper_content.replace("TITLE", title)
    if pdf!=None:
        paper_content = paper_content + "            <a href=\"PDF\"> <img src=\"images/pdf.png\" width=\"25\" height=\"25\"></a>\n".replace("PDF", pdf)
    if tool!=None:
        paper_content = paper_content + "            <a href=\"TOOL\"> <img src=\"images/github.png\" width=\"25\" height=\"25\"></a>\n".replace("TOOL", tool)
    if video!=None:
        paper_content = paper_content + "            <a href=\"VIDEO\"> <img src=\"images/video.png\" width=\"25\" height=\"25\"></a>\n".replace("VIDEO", video)
    if ppt!=None:
        paper_content = paper_content + "            <a href=\"PPT\"> <img src=\"images/ppt.png\" width=\"25\" height=\"25\"></a>\n".replace("PPT", ppt)
    paper_template = paper_content + "            </h4>\n\
            AUTHOR.\n\
          <p class=\"\">CONF, YEAR.</p>\n\
          </li>\n"
    paper_content = paper_template.replace("AUTHOR", author).replace("CONF", conference).replace("YEAR", year)
    if award!=None:
        paper_content = paper_content + "            <p><span style=\"color:red\">"+award+"</span></p>"
    return paper_content
    

def build_selected_paper_list():
    with open('data/paper.json') as json_file:
        papers = json.load(json_file)
    paper_list_content="<h3><strong>Selected Research Papers</strong></h3>\n\
        <ul class=\"\">\n"
    for paper in papers:
        if(paper["is_selected"]):
            paper_content = build_paper(paper["title"], ", ".join(paper["authors"]), \
                                        paper["conference"], str(paper["year"]), \
                                        paper["pdf"], paper["tool"], paper["video"], paper["ppt"], paper["award"])
            paper_list_content = paper_list_content + paper_content
    paper_list_content = paper_list_content + "        </ul>"
    return paper_list_content
        
def build_student(name, image, degree, grade, direction, placement):
    student_content = "          <div class=\"col-md-2 col-sm-4 custom-column\">\n \
            <div class=\"thumbnail\">\n \
              <img class=\"img-circle student-img\" alt=\"...\"\n \
                src=\"IMG\">\n \
              <p class=\"header\">NAME</p>\n \
              <p class=\"b\">DEGREE GRADE</p>\n"
    student_content = student_content.replace("NAME", name).replace("IMG", image)\
                                     .replace("DEGREE", degree)
    if grade!="None":
        student_content = student_content.replace("GRADE", grade)
    else:
        student_content = student_content.replace(" GRADE", "")
    if direction!=None:
        student_content = student_content + "<p class=\"b\">" + direction + "</p>\n"
    if placement!=None:
        student_content = student_content + "<p class=\"b\">" + placement + "</p>\n"
    student_content += "            </div>\n \
          </div>\n"
    return student_content
                                

def build_student_list():
    with open('data/student.json') as json_file:
        students = json.load(json_file)
    student_list_content = "        <h3><strong>Students</strong></h3>\n \
        <div class=\"row custom-row\">\n"
    # current students
    for student in students["students"]:
        student_content = build_student(student["name"], student["image"], student["degree"],\
                                        str(student["grade"]), student["direction"], None)
        student_list_content = student_list_content + student_content
    student_list_content = student_list_content + "        </div>\n"

    # Former students
    student_list_content = student_list_content + "        <br>\n \
        <h3><strong>Former Students</strong></h3>\n \
        <div class=\"row custom-row\">\n"
    for student in students["former_students"]:
        student_content = build_student(student["name"], student["image"], student["degree"],\
                                        str(student["grade"]), None, student["placement"],)
        student_list_content = student_list_content + student_content
    student_list_content = student_list_content + "        </div>\n"

    return student_list_content

index_template_content = read_file(index_template_file)
# paper_content = build_selected_paper_list()
student_content = build_student_list()
generate_main(index_template_content, None, student_content)