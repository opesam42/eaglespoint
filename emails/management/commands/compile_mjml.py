from django.core.management.base import BaseCommand
import os
from django.conf import settings
from emails.mjml import load_mjml_from_file, compile_mjml

class Command(BaseCommand):
    help = "Convert MJML file to HTML email template"
    
    def add_arguments(self, parser):
        pass
        
    def handle(self, *args, **kwargs):
        input_folder = os.path.join(settings.BASE_DIR, 'emails', 'templates', 'mjml')
        output_folder = os.path.join(settings.BASE_DIR, 'emails', 'templates', 'compiled')

        if not os.path.exists(input_folder):
            self.stdout.write(self.style.ERROR(f"Input folder does not exist {input_folder}"))
            return

        os.makedirs(output_folder, exist_ok=True) #create output directory if it is not created

        mjml_files = [f for f in os.listdir(input_folder) if f.endswith(".mjml")]

        if not mjml_files:
            self.stdout.write(self.style.ERROR("No MJML files found in this folder"))
            return
        
        success_count = 0

        for file_name in mjml_files:
            mjml_path = os.path.join(input_folder, file_name)
            base_name = os.path.splitext(file_name)[0]
            output_file = os.path.join(output_folder, f"{base_name}.html")

            self.stdout.write(f"Compiling {output_file}...")

            mjml_content = load_mjml_from_file(mjml_path)
            if not mjml_content:
                self.stdout.write(self.style.ERROR(f"Could not load {mjml_path}"))
                continue

            html = compile_mjml(mjml_content, output_file)
            if html:
                success_count += 1
                self.stdout.write(self.style.SUCCESS(f"Saved: {output_file}"))
            else:
                self.stdout.write(self.style.ERROR(f"Failed to compile: {file_name}"))
        
        self.stdout.write(self.style.SUCCESS(f"\n✅ {success_count}/{len(mjml_files)} MJML files compiled successfully."))