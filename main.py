from canvasapi import Canvas
import tkinter as tk
import os
import re

class CanvasImporterApp:
    def __init__(self):
        self.root = tk.Tk()
        root = self.root
        root.title("Canvas importer")

        # Storing the desired width and height as variables
        width=800
        height=600
        # Retrieving the user's
        user_width = root.winfo_screenwidth()
        user_height = root.winfo_screenheight()
        x_pos = (user_width // 2) - (width // 2)
        y_pos = (user_height // 2) - (height // 2)
        root.geometry(f"{width}x{height}+{x_pos}+{y_pos}")

        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)

        self.frame_1 = tk.Frame(root, bg="#131417")
        self.frame_1.grid(row=0, column=0, sticky="nsew")
        self.course_entry = tk.Entry(self.frame_1, bg="#131417", fg="white", insertbackground="white")
        self.key_entry = tk.Entry(self.frame_1, bg="#131417", fg="white", insertbackground="white")

        self.frame_2 = tk.Frame(root)

        self.intro_page()
        self.help_page()

        # self.show_frame(self.frame_1)

    def intro_page(self):
        frame_1 = self.frame_1

        api_key_validation = self.api_key_validation
        frame_1.grid(row=0, column=0)
        intro_headline = tk.Label(
            frame_1,
            text="Velkommen til Canvas importer!",
            bg = "#131417",
            fg = "white",
        )
        intro_headline.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        intro_text = tk.Label(
            frame_1,
            text="Dette programmet lar deg importere innhold fra Canvas moduler, slik at du får det enkelt nedlastet lokalt på egen maskin.",
            bg="#131417",
            fg="white",
            wraplength=700
        )
        intro_text.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        # Instruction image
        # img = self.img
        # img_label = tk.Label(frame_1, image=img)
        # img_label.grid(row=2, column=1)

        # Course number text
        course_text = tk.Label(
            frame_1,
            text="Kurs ID",
            bg="#131417",
            fg="white",
        )
        course_text.grid(row=2, column=0)

        # Course number entry
        self.course_entry = tk.Entry(frame_1)
        course_entry = self.course_entry
        course_entry.grid(row=3, column=0)

        # API Key Text
        api_text = tk.Label(
            frame_1,
            text="API Nøkkel",
            bg="#131417",
            fg="white",
        )
        api_text.grid(row=4, column=0)


        # API Key entry
        self.key_entry = tk.Entry(frame_1)
        key_entry = self.key_entry
        key_entry.grid(row=5, column=0)
        # Makes it so that the user can submit the API key by pressing the Enter button
        key_entry.bind("<Return>", api_key_validation)

        # Import button
        import_btn = tk.Button(
            frame_1,
            text="Importer Moduler",
            command=api_key_validation,
            bg="#333333",
            fg="white"
        )
        import_btn = import_btn
        import_btn.grid(row=6, column=0, padx=10, pady=10)

    def help_page(self):
        frame_2 = self.frame_2

    def api_key_validation(self, event=None):
        API_KEY = self.key_entry.get()
        course_id = self.course_entry.get()

        if not API_KEY or not course_id:
            print("Invalid key or course ID")
            return

        API_URL = "https://jobloop.instructure.com/"
        try:
            # Initialize Canvas API
            canvas = Canvas(API_URL, API_KEY)

            # Get the course by ID
            course = canvas.get_course(course_id)
            course_name = re.sub(r'[<>:"/\\|?*]', '-', course.name)  # Sanitize course name
            print(f"Downloading modules for course: {course_name}")

            # Create a directory named after the course
            base_dir = os.path.join(os.getcwd(), course_name)
            os.makedirs(base_dir, exist_ok=True)

            # Add Canvas CSS URLs
            css_urls = [
                "https://du11hjcvx0uqb.cloudfront.net/dist/brandable_css/new_styles_normal_contrast/bundles/common-24f5d746c8.css",
                "https://du11hjcvx0uqb.cloudfront.net/dist/brandable_css/new_styles_normal_contrast/bundles/assignments-9538b12c90.css",
                "https://du11hjcvx0uqb.cloudfront.net/dist/brandable_css/7a3ce318970b54c230f06a22d5742f40/variables-7dd4b80918af0e0218ec0229e4bd5873.css",
                "https://du11hjcvx0uqb.cloudfront.net/dist/brandable_css/new_styles_normal_contrast/bundles/side_tabs_table-07e53264f5.css",
                "https://du11hjcvx0uqb.cloudfront.net/dist/brandable_css/no_variables/bundles/fonts-6ee09b0b2f.css",
                "https://du11hjcvx0uqb.cloudfront.net/dist/brandable_css/new_styles_normal_contrast/jst/PaginatedView-8a926fc28b.css",
                "https://du11hjcvx0uqb.cloudfront.net/dist/brandable_css/new_styles_normal_contrast/jst/TreeBrowser-44c6024769.css",
                "https://du11hjcvx0uqb.cloudfront.net/dist/brandable_css/new_styles_normal_contrast/bundles/new_user_tutorials-6b15f87caf.css",
                "https://du11hjcvx0uqb.cloudfront.net/dist/brandable_css/new_styles_normal_contrast/bundles/wiki_page-9ab9e5b496.css",
                "https://du11hjcvx0uqb.cloudfront.net/dist/brandable_css/new_styles_normal_contrast/bundles/common-415ae5938a.css",
                "https://du11hjcvx0uqb.cloudfront.net/dist/brandable_css/7a3ce318970b54c230f06a22d5742f40/variables-7dd4b80918af0e0218ec0229e4bd5873.css",
                "https://du11hjcvx0uqb.cloudfront.net/dist/brandable_css/no_variables/bundles/fonts-6ee09b0b2f.css"
                
            ]

            # Iterate through all modules in the course
            modules = course.get_modules()
            for module in modules:
                try:
                    # Sanitize module name
                    module_name = re.sub(r'[<>:"/\\|?*]', '-', module.name).strip()
                    module_dir = os.path.join(base_dir, module_name)

                    # Create a subfolder for the module
                    os.makedirs(module_dir, exist_ok=True)
                    print(f"Processing module: {module_name}")

                    # Download all pages in the module
                    for item in module.get_module_items():
                        if item.type == "Page":
                            try:
                                page = course.get_page(item.page_url)
                                page_title = re.sub(r'[<>:"/\\|?*]', '-', page.title).strip()  # Sanitize page title
                                page_file = os.path.join(module_dir, f"{page_title}.html")

                                # Add CSS links to the HTML content
                                css_links = "\n".join(
                                    [f'<link rel="stylesheet" href="{css_url}">' for css_url in css_urls]
                                )

                                html_content = f"""
                                <!DOCTYPE html>
                                <html lang="en">
                                <head>
                                    <meta charset="UTF-8">
                                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                                    <title>{page.title}</title>
                                    {css_links}
                                </head>
                                <body>
                                    {page.body}
                                </body>
                                </html>
                                """

                                # Save the page content to an HTML file
                                with open(page_file, "w", encoding="utf-8") as f:
                                    f.write(html_content)
                                print(f"Downloaded page: {page_title}")
                            except Exception as page_error:
                                print(f"Error downloading page '{item.title}': {page_error}")

                except Exception as module_error:
                    print(f"Error processing module '{module.name}': {module_error}")

            print("All modules and pages have been successfully downloaded.")
        except Exception as e:
            print(f"Error: {e}")

    # def canvas_importer(self):


    def run(self):
        self.root.mainloop()

def main():
    app = CanvasImporterApp()
    app.run()

if __name__ == "__main__":
    main()