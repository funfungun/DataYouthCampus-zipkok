# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class BlogPost(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=30)
    content = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'blog_post'


class CategoryInfo(models.Model):
    zipcode = models.IntegerField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)
    category_info = models.JSONField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'category_info'


class DataEngCsv(models.Model):
    zipcode = models.IntegerField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)
    avg_size = models.FloatField(blank=True, null=True)
    avg_cost = models.FloatField(blank=True, null=True)
    place_code = models.IntegerField(blank=True, null=True)
    op_ratio = models.IntegerField(blank=True, null=True)
    total_deal = models.IntegerField(blank=True, null=True)
    month_fee_ratio = models.IntegerField(blank=True, null=True)
    new_ratio = models.IntegerField(blank=True, null=True)
    bus_stop = models.IntegerField(blank=True, null=True)
    art = models.IntegerField(blank=True, null=True)
    bike = models.IntegerField(blank=True, null=True)
    gym = models.IntegerField(blank=True, null=True)
    chatolic = models.IntegerField(blank=True, null=True)
    hospital = models.IntegerField(blank=True, null=True)
    perform_place = models.IntegerField(blank=True, null=True)
    park = models.IntegerField(blank=True, null=True)
    theater = models.IntegerField(blank=True, null=True)
    subway = models.IntegerField(blank=True, null=True)
    animal_hospital = models.IntegerField(blank=True, null=True)
    beatuy_care = models.IntegerField(blank=True, null=True)
    coin_karaoke = models.IntegerField(blank=True, null=True)
    liberary = models.IntegerField(blank=True, null=True)
    church = models.IntegerField(blank=True, null=True)
    big_mart = models.IntegerField(blank=True, null=True)
    gonggogng_gym = models.IntegerField(blank=True, null=True)
    cafe = models.IntegerField(blank=True, null=True)
    police_office = models.IntegerField(blank=True, null=True)
    daiso = models.IntegerField(blank=True, null=True)
    bar = models.IntegerField(blank=True, null=True)
    shopping_center = models.IntegerField(blank=True, null=True)
    super_market = models.IntegerField(blank=True, null=True)
    pharmacy = models.IntegerField(blank=True, null=True)
    banchan = models.IntegerField(blank=True, null=True)
    convience_store = models.IntegerField(blank=True, null=True)
    bank = models.IntegerField(blank=True, null=True)
    coin_wash_room = models.IntegerField(blank=True, null=True)
    yoga = models.IntegerField(blank=True, null=True)
    cross_fit = models.IntegerField(blank=True, null=True)
    atm = models.IntegerField(db_column='ATM', blank=True, null=True)  # Field name made lowercase.
    food_store = models.IntegerField(blank=True, null=True)
    post_office = models.IntegerField(blank=True, null=True)
    pc_room = models.IntegerField(db_column='PC_room', blank=True, null=True)  # Field name made lowercase.
    piilates = models.IntegerField(blank=True, null=True)
    citizen_center = models.IntegerField(blank=True, null=True)
    temple = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'data_eng_csv'


class DataEngCsv2(models.Model):
    zipcode = models.IntegerField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)
    avg_size = models.FloatField(blank=True, null=True)
    avg_cost = models.FloatField(blank=True, null=True)
    place_code = models.IntegerField(blank=True, null=True)
    op_ratio = models.IntegerField(blank=True, null=True)
    total_deal = models.IntegerField(blank=True, null=True)
    month_fee_ratio = models.IntegerField(blank=True, null=True)
    new_ratio = models.IntegerField(blank=True, null=True)
    bus_stop = models.IntegerField(blank=True, null=True)
    art = models.IntegerField(blank=True, null=True)
    bike = models.IntegerField(blank=True, null=True)
    gym = models.IntegerField(blank=True, null=True)
    chatolic = models.IntegerField(blank=True, null=True)
    hospital = models.IntegerField(blank=True, null=True)
    perform_place = models.IntegerField(blank=True, null=True)
    park = models.IntegerField(blank=True, null=True)
    theater = models.IntegerField(blank=True, null=True)
    subway = models.IntegerField(blank=True, null=True)
    animal_hospital = models.IntegerField(blank=True, null=True)
    beatuy_care = models.IntegerField(blank=True, null=True)
    coin_karaoke = models.IntegerField(blank=True, null=True)
    liberary = models.IntegerField(blank=True, null=True)
    church = models.IntegerField(blank=True, null=True)
    big_mart = models.IntegerField(blank=True, null=True)
    gonggogng_gym = models.IntegerField(blank=True, null=True)
    cafe = models.IntegerField(blank=True, null=True)
    police_office = models.IntegerField(blank=True, null=True)
    daiso = models.IntegerField(blank=True, null=True)
    bar = models.IntegerField(blank=True, null=True)
    shopping_center = models.IntegerField(blank=True, null=True)
    super_market = models.IntegerField(blank=True, null=True)
    pharmacy = models.IntegerField(blank=True, null=True)
    banchan = models.IntegerField(blank=True, null=True)
    convience_store = models.IntegerField(blank=True, null=True)
    bank = models.IntegerField(blank=True, null=True)
    coin_wash_room = models.IntegerField(blank=True, null=True)
    yoga = models.IntegerField(blank=True, null=True)
    cross_fit = models.IntegerField(blank=True, null=True)
    atm = models.IntegerField(db_column='ATM', blank=True, null=True)  # Field name made lowercase.
    food_store = models.IntegerField(blank=True, null=True)
    post_office = models.IntegerField(blank=True, null=True)
    pc_room = models.IntegerField(db_column='PC_room', blank=True, null=True)  # Field name made lowercase.
    piilates = models.IntegerField(blank=True, null=True)
    citizen_center = models.IntegerField(blank=True, null=True)
    temple = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'data_eng_csv_2'


class DataEngCsv3(models.Model):
    zipcode = models.IntegerField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)
    avg_size = models.FloatField(blank=True, null=True)
    avg_cost = models.FloatField(blank=True, null=True)
    place_code = models.IntegerField(blank=True, null=True)
    op_ratio = models.IntegerField(blank=True, null=True)
    total_deal = models.IntegerField(blank=True, null=True)
    month_fee_ratio = models.FloatField(blank=True, null=True)
    new_ratio = models.IntegerField(blank=True, null=True)
    atm = models.IntegerField(blank=True, null=True)
    pc_room = models.IntegerField(blank=True, null=True)
    police_office = models.IntegerField(blank=True, null=True)
    gonggogng_gym = models.IntegerField(blank=True, null=True)
    perform_place = models.IntegerField(blank=True, null=True)
    park = models.IntegerField(blank=True, null=True)
    church = models.IntegerField(blank=True, null=True)
    big_mart = models.IntegerField(blank=True, null=True)
    liberary = models.IntegerField(blank=True, null=True)
    animal_hospital = models.IntegerField(blank=True, null=True)
    art = models.IntegerField(blank=True, null=True)
    banchan = models.IntegerField(blank=True, null=True)
    bus_stop = models.IntegerField(blank=True, null=True)
    hospital = models.IntegerField(blank=True, null=True)
    beauty_care = models.IntegerField(blank=True, null=True)
    daiso = models.IntegerField(blank=True, null=True)
    chatolic = models.IntegerField(blank=True, null=True)
    shopping_center = models.IntegerField(blank=True, null=True)
    bar = models.IntegerField(blank=True, null=True)
    super_market = models.IntegerField(blank=True, null=True)
    pharmacy = models.IntegerField(blank=True, null=True)
    theater = models.IntegerField(blank=True, null=True)
    yoga = models.IntegerField(blank=True, null=True)
    post_office = models.IntegerField(blank=True, null=True)
    bank = models.IntegerField(blank=True, null=True)
    food_store = models.IntegerField(blank=True, null=True)
    bike = models.IntegerField(blank=True, null=True)
    temple = models.IntegerField(blank=True, null=True)
    citizen_center = models.IntegerField(blank=True, null=True)
    subway = models.IntegerField(blank=True, null=True)
    cafe = models.IntegerField(blank=True, null=True)
    coin_karaoke = models.IntegerField(blank=True, null=True)
    coin_wash_room = models.IntegerField(blank=True, null=True)
    cross_fit = models.IntegerField(blank=True, null=True)
    convience_store = models.IntegerField(blank=True, null=True)
    piilates = models.IntegerField(blank=True, null=True)
    gym = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'data_eng_csv_3'


class DataEngCsv4(models.Model):
    zipcode = models.IntegerField(primary_key=True,blank=True, null=False)
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)
    avg_size = models.FloatField(blank=True, null=True)
    avg_cost = models.FloatField(blank=True, null=True)
    place_code = models.IntegerField(blank=True, null=True)
    dd = models.IntegerField(blank=True, null=True)
    yl = models.IntegerField(blank=True, null=True)
    op = models.IntegerField(blank=True, null=True)
    total_deal = models.IntegerField(blank=True, null=True)
    avg_year = models.FloatField(blank=True, null=True)
    month_fee_ratio = models.FloatField(blank=True, null=True)
    new_ratio = models.IntegerField(blank=True, null=True)
    atm = models.IntegerField(blank=True, null=True)
    pc_room = models.IntegerField(blank=True, null=True)
    police_office = models.IntegerField(blank=True, null=True)
    gonggogng_gym = models.IntegerField(blank=True, null=True)
    perform_place = models.IntegerField(blank=True, null=True)
    park = models.IntegerField(blank=True, null=True)
    church = models.IntegerField(blank=True, null=True)
    big_mart = models.IntegerField(blank=True, null=True)
    liberary = models.IntegerField(blank=True, null=True)
    animal_hospital = models.IntegerField(blank=True, null=True)
    art = models.IntegerField(blank=True, null=True)
    banchan = models.IntegerField(blank=True, null=True)
    bus_stop = models.IntegerField(blank=True, null=True)
    hospital = models.IntegerField(blank=True, null=True)
    beauty_care = models.IntegerField(blank=True, null=True)
    daiso = models.IntegerField(blank=True, null=True)
    chatolic = models.IntegerField(blank=True, null=True)
    shopping_center = models.IntegerField(blank=True, null=True)
    bar = models.IntegerField(blank=True, null=True)
    super_market = models.IntegerField(blank=True, null=True)
    pharmacy = models.IntegerField(blank=True, null=True)
    theater = models.IntegerField(blank=True, null=True)
    yoga = models.IntegerField(blank=True, null=True)
    post_office = models.IntegerField(blank=True, null=True)
    bank = models.IntegerField(blank=True, null=True)
    food_store = models.IntegerField(blank=True, null=True)
    cafe = models.IntegerField(blank=True, null=True)
    bike = models.IntegerField(blank=True, null=True)
    temple = models.IntegerField(blank=True, null=True)
    citizen_center = models.IntegerField(blank=True, null=True)
    subway = models.IntegerField(blank=True, null=True)
    coin_karaoke = models.IntegerField(blank=True, null=True)
    coin_wash_room = models.IntegerField(blank=True, null=True)
    cross_fit = models.IntegerField(blank=True, null=True)
    convience_store = models.IntegerField(blank=True, null=True)
    piilates = models.IntegerField(blank=True, null=True)
    gym = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'data_eng_csv_4'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class DjangoSite(models.Model):
    domain = models.CharField(unique=True, max_length=100)
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'django_site'


class InfoCategory(models.Model):
    zipcode = models.IntegerField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)
    atm = models.FloatField(blank=True, null=True)
    pc_room = models.FloatField(blank=True, null=True)
    police_office = models.FloatField(blank=True, null=True)
    gonggogng_gym = models.FloatField(blank=True, null=True)
    perform_place = models.FloatField(blank=True, null=True)
    park = models.FloatField(blank=True, null=True)
    church = models.FloatField(blank=True, null=True)
    big_mart = models.FloatField(blank=True, null=True)
    liberary = models.FloatField(blank=True, null=True)
    animal_hospital = models.FloatField(blank=True, null=True)
    art = models.FloatField(blank=True, null=True)
    banchan = models.FloatField(blank=True, null=True)
    bus_stop = models.FloatField(blank=True, null=True)
    hospital = models.FloatField(blank=True, null=True)
    beauty_care = models.FloatField(blank=True, null=True)
    daiso = models.FloatField(blank=True, null=True)
    chatolic = models.FloatField(blank=True, null=True)
    shopping_center = models.FloatField(blank=True, null=True)
    bar = models.FloatField(blank=True, null=True)
    super_market = models.FloatField(blank=True, null=True)
    pharmacy = models.FloatField(blank=True, null=True)
    theater = models.FloatField(blank=True, null=True)
    yoga = models.FloatField(blank=True, null=True)
    post_office = models.FloatField(blank=True, null=True)
    bank = models.FloatField(blank=True, null=True)
    food_store = models.FloatField(blank=True, null=True)
    bike = models.FloatField(blank=True, null=True)
    temple = models.FloatField(blank=True, null=True)
    citizen_center = models.FloatField(blank=True, null=True)
    subway = models.FloatField(blank=True, null=True)
    cafe = models.FloatField(blank=True, null=True)
    coin_karaoke = models.FloatField(blank=True, null=True)
    coin_wash_room = models.FloatField(blank=True, null=True)
    cross_fit = models.FloatField(blank=True, null=True)
    convience_store = models.FloatField(blank=True, null=True)
    piilates = models.FloatField(blank=True, null=True)
    gym = models.FloatField(blank=True, null=True)
    atm_info = models.TextField(blank=True, null=True)
    pc_room_info = models.TextField(blank=True, null=True)
    police_office_info = models.TextField(blank=True, null=True)
    gonggogng_gym_info = models.TextField(blank=True, null=True)
    perform_place_info = models.TextField(blank=True, null=True)
    park_info = models.TextField(blank=True, null=True)
    church_info = models.TextField(blank=True, null=True)
    big_mart_info = models.TextField(blank=True, null=True)
    liberary_info = models.TextField(blank=True, null=True)
    animal_hospital_info = models.TextField(blank=True, null=True)
    art_info = models.JSONField(blank=True, null=True)
    banchan_info = models.TextField(blank=True, null=True)
    bus_stop_info = models.TextField(blank=True, null=True)
    hospital_info = models.TextField(blank=True, null=True)
    beauty_care_info = models.TextField(blank=True, null=True)
    daiso_info = models.TextField(blank=True, null=True)
    chatolic_info = models.TextField(blank=True, null=True)
    shopping_center_info = models.TextField(blank=True, null=True)
    bar_info = models.TextField(blank=True, null=True)
    super_market_info = models.TextField(blank=True, null=True)
    pharmacy_info = models.TextField(blank=True, null=True)
    theater_info = models.TextField(blank=True, null=True)
    yoga_info = models.TextField(blank=True, null=True)
    post_office_info = models.TextField(blank=True, null=True)
    bank_info = models.TextField(blank=True, null=True)
    food_store_info = models.TextField(blank=True, null=True)
    bike_info = models.TextField(blank=True, null=True)
    temple_info = models.JSONField(blank=True, null=True)
    citizen_center_info = models.TextField(blank=True, null=True)
    subway_info = models.TextField(blank=True, null=True)
    cafe_info = models.TextField(blank=True, null=True)
    coin_karaoke_info = models.TextField(blank=True, null=True)
    coin_wash_room_info = models.TextField(blank=True, null=True)
    cross_fit_info = models.TextField(blank=True, null=True)
    convience_store_info = models.TextField(blank=True, null=True)
    piilates_info = models.TextField(blank=True, null=True)
    gym_info = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'info_category'


class Jido(models.Model):
    bas_id = models.IntegerField(primary_key=True,db_column='BAS_ID', blank=True, null=False)  # Field name made lowercase.
    coordinates = models.JSONField(db_column='Coordinates', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'jido'


class PlzCategory(models.Model):
    zipcode = models.IntegerField(primary_key=True,null=False)
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)
    atm = models.FloatField(blank=True, null=True)
    pc_room = models.FloatField(blank=True, null=True)
    police_office = models.FloatField(blank=True, null=True)
    gonggogng_gym = models.FloatField(blank=True, null=True)
    perform_place = models.FloatField(blank=True, null=True)
    park = models.FloatField(blank=True, null=True)
    church = models.FloatField(blank=True, null=True)
    big_mart = models.FloatField(blank=True, null=True)
    liberary = models.FloatField(blank=True, null=True)
    animal_hospital = models.FloatField(blank=True, null=True)
    art = models.FloatField(blank=True, null=True)
    banchan = models.FloatField(blank=True, null=True)
    bus_stop = models.FloatField(blank=True, null=True)
    hospital = models.FloatField(blank=True, null=True)
    beauty_care = models.FloatField(blank=True, null=True)
    daiso = models.FloatField(blank=True, null=True)
    chatolic = models.FloatField(blank=True, null=True)
    shopping_center = models.FloatField(blank=True, null=True)
    bar = models.FloatField(blank=True, null=True)
    super_market = models.FloatField(blank=True, null=True)
    pharmacy = models.FloatField(blank=True, null=True)
    theater = models.FloatField(blank=True, null=True)
    yoga = models.FloatField(blank=True, null=True)
    post_office = models.FloatField(blank=True, null=True)
    bank = models.FloatField(blank=True, null=True)
    food_store = models.FloatField(blank=True, null=True)
    bike = models.FloatField(blank=True, null=True)
    temple = models.FloatField(blank=True, null=True)
    citizen_center = models.FloatField(blank=True, null=True)
    subway = models.FloatField(blank=True, null=True)
    cafe = models.FloatField(blank=True, null=True)
    coin_karaoke = models.FloatField(blank=True, null=True)
    coin_wash_room = models.FloatField(blank=True, null=True)
    cross_fit = models.FloatField(blank=True, null=True)
    convience_store = models.FloatField(blank=True, null=True)
    piilates = models.FloatField(blank=True, null=True)
    gym = models.FloatField(blank=True, null=True)
    atm_info = models.TextField(blank=True, null=True)
    pc_room_info = models.TextField(blank=True, null=True)
    police_office_info = models.TextField(blank=True, null=True)
    gonggogng_gym_info = models.TextField(blank=True, null=True)
    perform_place_info = models.TextField(blank=True, null=True)
    park_info = models.TextField(blank=True, null=True)
    church_info = models.TextField(blank=True, null=True)
    big_mart_info = models.TextField(blank=True, null=True)
    liberary_info = models.TextField(blank=True, null=True)
    animal_hospital_info = models.TextField(blank=True, null=True)
    art_info = models.TextField(blank=True, null=True)
    banchan_info = models.TextField(blank=True, null=True)
    bus_stop_info = models.TextField(blank=True, null=True)
    hospital_info = models.TextField(blank=True, null=True)
    beauty_care_info = models.TextField(blank=True, null=True)
    daiso_info = models.TextField(blank=True, null=True)
    chatolic_info = models.TextField(blank=True, null=True)
    shopping_center_info = models.TextField(blank=True, null=True)
    bar_info = models.TextField(blank=True, null=True)
    super_market_info = models.TextField(blank=True, null=True)
    pharmacy_info = models.TextField(blank=True, null=True)
    theater_info = models.TextField(blank=True, null=True)
    yoga_info = models.TextField(blank=True, null=True)
    post_office_info = models.TextField(blank=True, null=True)
    bank_info = models.TextField(blank=True, null=True)
    food_store_info = models.TextField(blank=True, null=True)
    bike_info = models.TextField(blank=True, null=True)
    temple_info = models.TextField(blank=True, null=True)
    citizen_center_info = models.TextField(blank=True, null=True)
    subway_info = models.TextField(blank=True, null=True)
    cafe_info = models.TextField(blank=True, null=True)
    coin_karaoke_info = models.TextField(blank=True, null=True)
    coin_wash_room_info = models.TextField(blank=True, null=True)
    cross_fit_info = models.TextField(blank=True, null=True)
    convience_store_info = models.TextField(blank=True, null=True)
    piilates_info = models.TextField(blank=True, null=True)
    gym_info = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'plz_category'


class PyboAnswer(models.Model):
    id = models.BigAutoField(primary_key=True)
    content = models.TextField()
    create_date = models.DateTimeField()
    question = models.ForeignKey('PyboQuestion', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'pybo_answer'


class PyboQuestion(models.Model):
    id = models.BigAutoField(primary_key=True)
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'pybo_question'


class TitlePost(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=30)
    content = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'title_post'


class WorkingBackAnswer(models.Model):
    id = models.BigAutoField(primary_key=True)
    content = models.TextField()
    create_date = models.DateTimeField()
    question = models.ForeignKey('WorkingBackQuestion', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'working_back_answer'


class WorkingBackQuestion(models.Model):
    id = models.BigAutoField(primary_key=True)
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'working_back_question'
