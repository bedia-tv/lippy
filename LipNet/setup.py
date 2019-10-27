from setuptools import setup

setup(name='lipnet',
    version='0.1.6',
    description='End-to-end sentence-level lipreading',
    url='http://github.com/rizkiarm/LipNet',
    author='Muhammad Rizki A.R.M',
    author_email='rizki@rizkiarm.com',
    license='MIT',
    packages=['lipnet'],
    zip_safe=False,
	install_requires=[
        'Keras>=2.0.2',
        'editdistance>=0.3.1',
		'h5py>=2.6.0',
		'matplotlib>=2.0.0',
		'numpy>=1.16.4',
		'python-dateutil>=2.6.0',
		'scipy>=1.3.0',
		'Pillow>=4.1.0',
		'tensorflow>=1.14',
		'Theano>=1.0.0',
        'nltk>=3.2.2',
        'sk-video>=1.1.10',
        'dlib>=19.18.0'
    ])
