from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager,AbstractUser
from shortuuidfield import ShortUUIDField
from django.db import models

class UserManager(BaseUserManager):
    def _create_user(self,telephone,username,password,**kwargs):
        if not username:
            raise ValueError('请输入用户名')
        if not telephone:
            raise ValueError('请输入电话号码')
        if not password:
            raise ValueError('请输入密码')
        user = self.model(username=username,telephone=telephone,**kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_user(self,telephone,username,password,**kwargs):
        kwargs['is_superuser'] = False
        return self._create_user(telephone,username,password,**kwargs)

    def create_superuser(self,telephone,username,password,**kwargs):
        kwargs['is_staff'] = True
        kwargs['is_superuser'] = True
        return self._create_user(telephone,username,password,**kwargs)

class User(AbstractBaseUser,PermissionsMixin):
    uuid = ShortUUIDField(primary_key=True)
    telephone = models.CharField(max_length=11,unique=True)
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True,null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    data_join = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'telephone'
    REQUIRED_FIELDS = ['username']
    EMALI_FIELD = 'emali'

    objects = UserManager()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return  self.username






