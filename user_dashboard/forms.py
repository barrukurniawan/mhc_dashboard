from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import CustomUser, UserBusiness, Province, City, GroupBusiness
from datetime import datetime, timedelta

class CustomUserCreationForm(UserCreationForm):
	def __init__(self, *args, **kargs):
		super(CustomUserCreationForm, self).__init__(*args, **kargs)
		self.fields['email'].widget.attrs.update({'class': 'form-control'})
		self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
		self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
		self.fields['password1'].widget.attrs.update({'class': 'form-control'})
		self.fields['password2'].widget.attrs.update({'class': 'form-control'})

	class Meta:
		model = CustomUser
		fields = ('email','first_name','last_name')

	def clean(self):
		email = self.cleaned_data.get('email')
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')

		if password1 != password2:
			raise ValidationError('Password & Password Confirmation tidak sama')

		else:
			try:
				CustomUser.objects.get(email=email)
			except CustomUser.DoesNotExist:
				return self.cleaned_data

			raise ValidationError('Email ' + email + ' sudah terdaftar')


class LoginForm(forms.Form):
	email = forms.EmailField(required=True)
	password = forms.CharField(widget=forms.PasswordInput(), required=True)

	email.widget.attrs.update({'class': 'form-control'})
	password.widget.attrs.update({'class': 'form-control', 'type': 'password'})


class OtpForm(forms.Form):
	otp = forms.CharField(max_length=5, required=True)
	otp.widget.attrs.update({'class': 'form-control'})


class BuyerForm(ModelForm):

	PROVINCE = (
			[('0', 'Pilih Provinsi')] +
			[(x.name, x.name) for x in Province.objects.all()]
	)

	CITY = (
			[('0', 'Pilih Kota')] +
			[(y.name, y.name) for y in City.objects.all()]
	)

	no_identification = forms.CharField(required=True, label='No KTP / NIK / Passport', max_length=16)
	first_name = forms.CharField(required=True, label='Nama Depan')
	last_name = forms.CharField(required=True, label='Nama Belakang')
	sex = forms.ChoiceField(required=True, choices=(
		('m', 'Pria'), ('f', 'Wanita')), label='Jenis Kelamin')
	birthday = forms.DateField(required=True, label='Tanggal Lahir', input_formats=['%d-%m-%Y'])
	address = forms.CharField(required=True, widget=forms.Textarea, label='Alamat Lengkap')
	email = forms.EmailField(required=True, label='Email')
	mobile_number = forms.CharField(required=True, max_length=15, label='No Handphone')
	province = forms.ChoiceField(choices=PROVINCE, initial=0, required=True, label='Provinsi')
	city = forms.ChoiceField(choices=CITY, initial=0, required=True, label='Kota')
	code_pos = forms.CharField(max_length=5, label='Kode Pos')


	no_identification.widget.attrs.update({'class': 'form-control'})
	first_name.widget.attrs.update({'class': 'form-control'})
	last_name.widget.attrs.update({'class': 'form-control'})
	sex.widget.attrs.update({'class': 'form-control'})
	birthday.widget.attrs.update({'class': 'form-control', 'placeholder': 'DD-MM-YYYY'})
	address.widget.attrs.update({'class': 'form-control', 'rows': 3})
	email.widget.attrs.update({'class': 'form-control'})
	province.widget.attrs.update({'class': 'form-control'})
	city.widget.attrs.update({'class': 'form-control'})
	code_pos.widget.attrs.update({'class': 'form-control'})
	mobile_number.widget.attrs.update({'class': 'form-control', 'placeholder': '08xxxxxxxxxx'})

	class Meta:
		model = CustomUser
		fields = ('no_identification', 'first_name', 'last_name', 'sex', 'birthday', 'address', 'email', 'mobile_number', 'code_pos', 'city', 'state')

	def clean(self):
		errors = []

		no_identification = self.cleaned_data['no_identification']
		mobile_number = self.cleaned_data['mobile_number']

		# Check Validation
		if mobile_number.isdigit() == False:
			errors.append('Phone hanya boleh di isi angka')

		if errors:
			raise ValidationError(errors)


class ResetPassForm(forms.Form):
	email = forms.EmailField(required=True)

	email.widget.attrs.update({'class': 'form-control'})

	def clean(self):
		email = self.cleaned_data.get('email')

		try:
			CustomUser.objects.get(email=email)
			return self.cleaned_data
		except CustomUser.DoesNotExist:
			raise ValidationError('Email ' + email + ' belum terdaftar')


class ChangePassword(forms.Form):
	old_pass = forms.CharField(label='Password Lama', widget=forms.PasswordInput(), required=True)
	new_pass = forms.CharField(label='Password Baru', widget=forms.PasswordInput(), required=True)
	confirm_pass = forms.CharField(label='Konfirmasi Password', widget=forms.PasswordInput(), required=True)

	old_pass.widget.attrs.update({'class': 'form-control'})
	new_pass.widget.attrs.update({'class': 'form-control'})
	confirm_pass.widget.attrs.update({'class': 'form-control'})


class GroupBusinessForm(ModelForm):
	company_name = forms.CharField(max_length=50, required=True, label='Nama PT/CV/Group Usaha')
	address = forms.CharField(widget=forms.Textarea, required=True, label='Alamat Usaha')
	mobile_number = forms.CharField(max_length=13, required=True, label='No Telepon Usaha')
	email = forms.CharField(max_length=50, required=True, label='Email')
	jenis_usaha = forms.CharField(max_length=30, required=True, label='Jenis Usaha')
	pic = forms.CharField(max_length=30, required=False, label='PIC')
	province = forms.CharField(max_length=30, required=False, label='Provinsi')
	city = forms.CharField(max_length=30, required=False, label='Kota')
	pulau = forms.CharField(max_length=30, required=False, label='Pulau')
	tipe_sistem = forms.CharField(max_length=100, required=False, label='Penerapan Sistem')
	rating = forms.CharField(max_length=1, required=False, label='Rating')

	company_name.widget.attrs.update({'class': 'form-control'})
	email.widget.attrs.update({'class': 'form-control'})
	mobile_number.widget.attrs.update({'class': 'form-control'})
	address.widget.attrs.update({'class': 'form-control', 'style':'height:150px'})
	jenis_usaha.widget.attrs.update({'class': 'form-control'})
	pic.widget.attrs.update({'class': 'form-control'})
	city.widget.attrs.update({'class': 'form-control'})
	province.widget.attrs.update({'class': 'form-control'})
	pulau.widget.attrs.update({'class': 'form-control'})
	tipe_sistem.widget.attrs.update({'class': 'form-control'})
	rating.widget.attrs.update({'class': 'form-control'})

	class Meta:
		model = GroupBusiness
		fields = ('company_name','address','mobile_number','email', 'jenis_usaha', 'pic', 'tipe_sistem', 'rating', 'pulau', 'province', 'city')

class UserBusinessForm(ModelForm):
    first_name = forms.CharField(max_length=20, required=False, label='Nama Depan')
    last_name = forms.CharField(max_length=20, required=False, label='Nama Belakang')
    email = forms.EmailField(required=True, label='Email')
    status = forms.CharField(max_length=20, required=False, label='Posisi')
    role = forms.ChoiceField(choices=(('Marketing Manager', 'Marketing Manager'), ('Entry data staff', 'Entry data staff')), required=False, label='Role')
    wilayah = forms.ChoiceField(choices=(('1', 'Surabaya,Gresik,Sidoarjo'), ('2', 'Pasuruan,Malang ke timur'), ('3', 'Mojokerto ke barat'), ('4','Jawa Tengah'), ('5','Jawa Barat'), ('6','Jakarta'), ('7','Bali, Nusa Tenggara, Maluku dan Papua'), ('8','Kalimantan dan Sulawesi'), ('9','Aceh, Sumut dan Sumbar'), ('10','Sumsel, Lampung, Batam dan Kep. Riau')), required=False, label='Wilayah')

    first_name.widget.attrs.update({'class': 'form-control'})
    status.widget.attrs.update({'class': 'form-control'})
    last_name.widget.attrs.update({'class': 'form-control'})
    email.widget.attrs.update({'class': 'form-control'})
    role.widget.attrs.update({'class': 'form-control'})
    wilayah.widget.attrs.update({'class': 'form-control'})

    class Meta:
    	model = UserBusiness
    	fields = ('first_name', 'last_name', 'email', 'status', 'role', 'wilayah')
    def clean(self):
    	email = self.cleaned_data['email']
    	try:
    		CustomUser.objects.get(email=email)
    	except CustomUser.DoesNotExist:
    		return self.cleaned_data
    	raise ValidationError('Email ' + email + ' sudah terdaftar')

class userDetailForm(ModelForm):
	# PROVINCE = (
	# 		[('0', 'Pilih Provinsi')] +
	# 		[(x.name, x.name) for x in Province.objects.all()]
	# )

	# CITY = (
	# 		[('0', 'Pilih Kota')] +
	# 		[(y.name, y.name) for y in City.objects.all()]
	# )

	no_identification = forms.CharField(max_length=16, required=False, label='No KTP / Passport')
	full_name = forms.CharField(max_length=20, required=False, label='Nama')
	first_name = forms.CharField(max_length=20, required=False, label='Nama Depan')
	last_name = forms.CharField(max_length=20, required=False, label='Nama Belakang')
	sex = forms.ChoiceField(choices=(
		('m', 'Pria'), ('f', 'Wanita')), required=False, label='Jenis Kelamin')
	birthday = forms.DateField(required=False, input_formats=['%d-%m-%Y'], label='Tanggal Lahir')
	email = forms.EmailField(required=True, label='Email')
	status = forms.CharField(max_length=20, required=False, label='Status')
	mobile_number = forms.CharField(max_length=12,required=False, label='No Handphone')
	address = forms.CharField(widget=forms.Textarea, required=False, label='Alamat Lengkap')
	state = forms.CharField(max_length=100, required=False, label='Provinsi')
	city = forms.CharField(max_length=100, required=False, label='Kota')
	code_pos = forms.CharField(max_length=5, required=False, label='Kode Pos')

	no_identification.widget.attrs.update({'class': 'form-control'})
	full_name.widget.attrs.update({'class': 'form-control'})
	first_name.widget.attrs.update({'class': 'form-control'})
	last_name.widget.attrs.update({'class': 'form-control'})
	sex.widget.attrs.update({'class': 'form-control'})
	status.widget.attrs.update({'class': 'form-control'})
	birthday.widget.attrs.update({'class': 'form-control'})
	address.widget.attrs.update({'class': 'form-control', 'rows': 3})
	email.widget.attrs.update({'class': 'form-control', 'readonly': 'readonly'})
	mobile_number.widget.attrs.update({'class': 'form-control'})
	code_pos.widget.attrs.update({'class': 'form-control'})
	city.widget.attrs.update({'class': 'form-control'})
	state.widget.attrs.update({'class': 'form-control'})

	class Meta:
		model = CustomUser
		fields = ('no_identification', 'full_name', 'first_name', 'last_name', 'mobile_number', 'sex', 'birthday', 'address', 'email', 'code_pos', 'city', 'state')

class CompanyListForm(forms.Form):
    status = forms.ChoiceField(choices=(('Active', 'true'), ('Inactive', 'false')))
    date_from = forms.DateField(label='Tanggal Awal', input_formats=['%d/%m/%Y'], initial=(datetime.now() - timedelta(days=365)).strftime('%d/%m/%Y'))
    date_to = forms.DateField(label='Tanggal Akhir', input_formats=['%d/%m/%Y'], initial=datetime.now().strftime('%d/%m/%Y'))
    ordering = forms.ChoiceField(label='Sortir', choices=(('-created_at', 'Terbaru'), ('created_at', 'Terlama')))

    status.widget.attrs.update({'class': 'form-control'})
    date_from.widget.attrs.update({'class': 'form-control'})
    date_to.widget.attrs.update({'class': 'form-control'})
    ordering.widget.attrs.update({'class': 'form-control'})