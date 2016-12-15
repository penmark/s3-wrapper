from distutils.core import setup

setup(name='s3_wrapper',
        version='1.0.0',
        description='s3 boto wrapper',
        author='Pontus Enmark',
        author_email='pontus@wka.se',
        url='https://github.com/penmark/s3-wrapper',
        packages=['s3_wrapper'],
        install_requires=[
            'boto==2.44.0',
            'python-dotenv==0.6.1'
            ],
        entry_points='''
        [console_scripts]
        s3 = s3_wrapper.main:main
        '''
        )
