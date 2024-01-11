from rest_framework import serializers
from .models import Folder,Files
import shutil
from zipfile import ZipFile, ZIP_DEFLATED
import pathlib
class FileListSerializer(serializers.Serializer):
    files = serializers.ListField(
        child = serializers.FileField(max_length = 100000 , allow_empty_file = False , use_url = False)
    )
    folder = serializers.CharField(required = False)
    
    def zip_files(self,folder):
        # Can use this to directly zip the folder or files
        # shutil.make_archive(f'public/media/zip/{folder}' , 'zip' ,f'public/media/{folder}' )

        # Using Zipfile to compress the files before creating the
        directory = pathlib.Path(f"public/media/{folder}")
        with ZipFile(f'public/media/zip/{folder}.zip', "w", ZIP_DEFLATED, compresslevel=9) as archive:
            for file_path in directory.rglob("*"):
                archive.write(file_path, arcname=file_path.relative_to(directory))
        
    def create(self , validated_data):
        folder = Folder.objects.create()
        files = validated_data.pop('files')
        files_objs = []
        for file in files:
            files_obj = Files.objects.create(folder = folder , file = file)
            files_objs.append(files_obj)
        self.zip_files(folder.uid)
        
        return {'files' : {} , 'folder' : str(folder.uid)}