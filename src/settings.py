import os
import sys
sys.path.append("..")

SQLALCHEMY_TRACK_MODIFICATIONS=False
SQLALCHEMY_DATABASE_URI = "postgresql://vgzucsdlhbrbcn:8491ba2aca4676cb76c8a18be7fcf85e4534c1e0ac3e35e16a6c20463745592a@ec2-34-193-113-223.compute-1.amazonaws.com:5432/d17jf8jsppcg3u"
# SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
SECRET_KEY = "supersecretkey"
# SECRET_KEY = os.environ.get('SECRET_KEY')