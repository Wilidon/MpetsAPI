from setuptools import setup

setup(name='mpets',
      version='0.5.46',
      description='API for game AmazingPets',
      packages=['mpets', 'mpets.utils', 'mpets.models'],
      author_email='wilidon@bk.ru',
      install_requires=[
          'python-box[all]',
          'aiohttp',
          'BeautifulSoup4',
          'lxml',
          'aiohttp-socks',
          'pydantic'
      ],
      zip_safe=False)
