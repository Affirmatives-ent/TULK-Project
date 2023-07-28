# storage.py

from cloudinary_storage.storage import MediaCloudinaryStorage


class CustomMediaCloudinaryStorage(MediaCloudinaryStorage):
    def path(self, name):
        if self.exists(name):
            return self.url(name)
        return name
