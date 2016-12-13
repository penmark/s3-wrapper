from distutils.core import setup

setup(name='S3',
        version='0.0.1',
        description='boto wrapper',
        author='Pontus Enmark',
        author_email='pontus@wka.se',
        url='https://wka.se/s3',
        packages=['s3'],
        install_requires=[
            'boto==2.44.0',
            'python-dotenv==0.6.1'
            ],
        entry_points='''
        [console_scripts]
        s3 = s3.main:main
        '''
        )
