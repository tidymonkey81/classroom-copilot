

import ai



# save the presentation with a filename including the topic id
def save_pptx(presentation, ppt_output_dir, ks, topic_id):
    # Check if the topic folder exists and if not, create it
    if not os.path.exists(ppt_output_dir + '\\KS' + str(ks)):
        os.makedirs(ppt_output_dir + '\\KS' + str(ks))
    presentation.SaveAs(ppt_output_dir + '\\KS' + str(ks) + '\\topic_' + topic_id + '.pptx')
    presentation.Close()

# Check if the topic powerpoint already exists
def check_pptx_exists(ppt_output_dir, ks, topic_id):
    # Check if the topic folder exists and if not, create it
    if not os.path.exists(ppt_output_dir + '\\KS' + str(ks)):
        os.makedirs(ppt_output_dir + '\\KS' + str(ks))
    if os.path.exists(ppt_output_dir + '\\KS' + str(ks) + '\\topic_' + topic_id + '.pptx'):
        return True
    else:
        return False    

def add_slide(presentation, slide_layout_index, title):
    # Add a new slide
    slide_layout = presentation.SlideMaster.CustomLayouts(slide_layout_index)
    slide = presentation.Slides.AddSlide(presentation.Slides.Count + 1, slide_layout)
    # If the title frame exists add the title
    if slide.Shapes.Count > 0 and slide.Shapes[0].Name == 'Title 1':
        title_frame = slide.Shapes.Title
        title_frame.TextFrame.TextRange.Text = title
    return slide

def add_section(presentation, section_number, section_name):
    # Add a new section
    section_index = presentation.SectionProperties.AddSection(section_number, section_name)
    return section_index

def add_slide_single_content(presentation, slide_layout_index, title, content):
    # Add a new slide
    slide_layout = presentation.SlideMaster.CustomLayouts(slide_layout_index)
    slide = presentation.Slides.AddSlide(presentation.Slides.Count + 1, slide_layout)
    # If the title frame exists add the title
    if slide.Shapes.Count > 0 and slide.Shapes[0].Name == 'Title 1':
        title_frame = slide.Shapes.Title
        title_frame.TextFrame.TextRange.Text = title
    # Add content
    slide.Shapes[1].TextFrame.TextRange.Text = content
    return slide

def add_slide_lesson_starter(presentation, slide_layout_index, title, content):
    # Add a new slide
    slide_layout = presentation.SlideMaster.CustomLayouts(slide_layout_index)
    slide = presentation.Slides.AddSlide(presentation.Slides.Count + 1, slide_layout)
    # If the title frame exists add the title
    if slide.Shapes.Count > 0 and slide.Shapes[0].Name == 'Title 1':
        title_frame = slide.Shapes.Title
        title_frame.TextFrame.TextRange.Text = title
    # Add content
    slide.Shapes[1].TextFrame.TextRange.Text = content
    return slide

# Function to add a new section and slide
def add_section_slide(presentation, section_number, section_name, slide_layout_index, slide_title):
    # Add a new section
    section_index = presentation.SectionProperties.AddSection(section_number, section_name)
    # Add a new slide
    slide_layout = presentation.SlideMaster.CustomLayouts(slide_layout_index)
    slide = presentation.Slides.AddSlide(presentation.Slides.Count + 1, slide_layout)
    # Move slide to new section
    slide.MoveToSectionStart(section_index)
    # If the title frame exists add the title
    if slide.Shapes.Count > 0 and slide.Shapes[0].Name == 'Title 1':
        title_frame = slide.Shapes.Title
        title_frame.TextFrame.TextRange.Text = slide_title
    return slide

# Function to add a new section and slide with single content
def add_section_slide_single_content(presentation, section_number, section_name, slide_layout_index, slide_title, content):
    # Add a new section
    section_index = presentation.SectionProperties.AddSection(section_number, section_name)
    # Add a new slide
    slide_layout = presentation.SlideMaster.CustomLayouts(slide_layout_index)
    slide = presentation.Slides.AddSlide(presentation.Slides.Count + 1, slide_layout)
    # Move slide to new section
    slide.MoveToSectionStart(section_index)
    # If the title frame exists add the title
    if slide.Shapes.Count > 0 and slide.Shapes[0].Name == 'Title 1':
        title_frame = slide.Shapes.Title
        title_frame.TextFrame.TextRange.Text = slide_title
    # Add content
    slide.Shapes[1].TextFrame.TextRange.Text = content
    return slide

# Function to add a lesson title section and slides
def add_lesson_title_section(presentation, section_number, section_name, cover_slide_layout_index, cover_slide_title, inner_slide_layout_index, inner_slide_title):
    # Add a new section and add a slide to the section
    cover_slide = add_section_slide(presentation, section_number, section_name, cover_slide_layout_index, cover_slide_title)

    # Add another slide to the section
    inner_slide = add_slide(presentation, inner_slide_layout_index, inner_slide_title)

    return cover_slide, inner_slide

# Function to check if the topic has a topic summary text file and if so, use it, otherwise generate one
def generate_topic_summary(prompt, text_output_dir, ks, topic_id):
    # Check if the topic summary text exists and if so, use it, otherwise generate one
    text_path = text_output_dir + '\\KS' + str(ks) + '\\' + topic_id + '\\topic_summary_' + topic_id + '.txt'
    if os.path.exists(text_path):
        print("Text exists")
        # Read the text file
        with open(text_path, 'r') as f:
            text = f.read()
    else:
        print("Text does not exist")
        # Generate a topic summary text
        chat_completion = ai.openai_user(prompt)
        text = chat_completion.choices[0].message.content
        if text:
            print("Generated Text:")
            print(text)
            # Save the text to a file
            # if the topic folder doesn't exist, create it
            if not os.path.exists(text_output_dir + '\\KS' + str(ks) + '\\' + topic_id):
                os.makedirs(text_output_dir + '\\KS' + str(ks) + '\\' + topic_id)
            with open(text_path, 'w') as f:
                f.write(text)
        else:
            print("Text is not generated")
    return text

# Function to check if the lesson has a lesson summary text file and if so, use it, otherwise generate one
def generate_lesson_summary(prompt, text_output_dir, ks, topic_id, lesson_id):
    # Check if the lesson summary text exists and if so, use it, otherwise generate one
    text_path = text_output_dir + '\\KS' + str(ks) + '\\' + topic_id + '\\lesson_summary_' + lesson_id + '.txt'
    if os.path.exists(text_path):
        print("Text exists")
        # Read the text file
        with open(text_path, 'r') as f:
            text = f.read()
    else:
        print("Text does not exist")
        # Generate a lesson summary text
        chat_completion = ai.openai_user(prompt)
        text = chat_completion.choices[0].message.content
        if text:
            print("Generated Text:")
            print(text)
            # Save the text to a file
            # if the topic folder doesn't exist, create it
            if not os.path.exists(text_output_dir + '\\KS' + str(ks) + '\\' + topic_id):
                os.makedirs(text_output_dir + '\\KS' + str(ks) + '\\' + topic_id)
            with open(text_path, 'w') as f:
                f.write(text)
        else:
            print("Text is not generated")
    return text

# A function to check if the topic title slide has a cover image file and if so, use it, otherwise generate one
def generate_topic_cover_image(topic_cover_prompt, image_output_dir, ks, topic_id, slides):
    # Check if the topic has a cover slide and if so, use it, otherwise generate one
    image_path = image_output_dir + '\\KS' + str(ks) + '\\' + topic_id + '\\topic_cover_slide_' + topic_id + '.jpg'
    print(image_path)
    if os.path.exists(image_path):
        print("Cover slide exists")
        # Add the picture to the cover slide and fill the slide
        slide = slides['cover_slide']
        # Assuming slide_width and slide_height are the dimensions of the slide
        
    else:
        print("Cover slide does not exist")
        # Create a cover slide
        model = "dall-e-3"
        prompt = topic_cover_prompt
        # Generate an image and get a URL from OpenAI
        image_url = ai.generate_image(model, prompt)
        if image_url:
            print("Generated Image URL:")
            print(image_url)
            # Download the image
            r = requests.get(image_url, stream=True)
            if r.status_code == 200:
                # if the topic folder doesn't exist, create it
                if not os.path.exists(image_output_dir + '\\KS' + str(ks) + '\\' + topic_id):
                    os.makedirs(image_output_dir + '\\KS' + str(ks) + '\\' + topic_id)
                with open(image_path, 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
            else:
                print('Image couldn\'t be retreived')
        else:
            print("Image URL is not generated")

        # Add the picture to the cover slide and send it to the back
        slide = slides['cover_slide']
        slide_width = slide.Master.Width
        slide_height = slide.Master.Height
        slide.Shapes.AddPicture(FileName=image_path, LinkToFile=0, SaveWithDocument=1, Left=0, Top=0, Width=slide_width, Height=slide_height)
        print(slide.Shapes)
        slide.Shapes(2).ZOrder(1)

# A function to check if the lesson title slide has a cover image file and if so, use it, otherwise generate one
def generate_lesson_cover_image(lesson_cover_prompt, image_output_dir, ks, topic_id, lesson_id, slides):
    image_path = image_output_dir + '\\KS' + str(ks) + '\\' + topic_id + '\\lesson_cover_slide_' + lesson_id + '.jpg'
    if os.path.exists(image_path):
        print("Cover slide exists")
        # Add the picture to the cover slide and fill the slide
        slide = slides['lesson_' + lesson_id]
        # Assuming slide_width and slide_height are the dimensions of the slide
        slide_width = slide.Master.Width
        slide_height = slide.Master.Height
        slide.Shapes.AddPicture(FileName=image_path, LinkToFile=0, SaveWithDocument=1, Left=0, Top=0, Width=slide_width, Height=slide_height)
        slide.Shapes(3).ZOrder(1)
    else:
        print("Cover slide does not exist")
        # Create a cover slide
        model = "dall-e-3"
        prompt = lesson_cover_prompt
        # Generate an image and get a URL from OpenAI
        image_url = ai.generate_image(model, prompt)
        if image_url:
            print("Generated Image URL:")
            print(image_url)
            # Download the image
            r = requests.get(image_url, stream=True)
            if r.status_code == 200:
                with open(image_path, 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
            else:
                print('Image couldn\'t be retreived')
        else:
            print("Image URL is not generated")

        # Add the picture to the cover slide and send it to the back
        slide = slides['lesson_' + lesson_id]
        slide_width = slide.Master.Width
        slide_height = slide.Master.Height
        slide.Shapes.AddPicture(FileName=image_path, LinkToFile=0, SaveWithDocument=1, Left=0, Top=0, Width=slide_width, Height=slide_height)
        print(slide.Shapes)
        slide.Shapes(3).ZOrder(1)