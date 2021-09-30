from django.db import models

class UserVo(models.Model):
    username = models.TextField(primary_key=True)
    password = models.CharField(max_length=10)
    name = models.TextField()
    email = models.EmailField()
    birth = models.TextField()
    address = models.TextField()

    class Meta:
        manage = True
        db_table = 'users'

    def __str__(self):
        return f'[{self.pk}] {self.username}'
