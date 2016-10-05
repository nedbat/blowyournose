from setuptools import setup

setup(
    name='BlowYourNose plugin',
    version='1.0',
    author='Ned Batchelder',
    author_email='ned@nedbatchelder.com',
    description='A nose plugin to clean out attributes on the test case',
    license='Apache 2.0',
    py_modules=['blowyournose'],
    entry_points={
        'nose.plugins.0.10': [
            'blowyournose = blowyournose:BlowYourNose'
        ]
    }
)
