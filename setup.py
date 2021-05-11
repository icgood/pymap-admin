# Copyright (c) 2021 Ian C. Good
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

from setuptools import setup, find_packages  # type: ignore

with open('README.md') as f:
    readme = f.read()

with open('LICENSE.md') as f:
    license = f.read()


setup(name='pymap-admin',
      version='0.7.1',
      author='Ian Good',
      author_email='ian@icgood.net',
      description='Admin tool for running pymap instances.',
      long_description=readme + license,
      long_description_content_type='text/markdown',
      license='MIT',
      url='https://github.com/icgood/pymap-admin/',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Topic :: Communications :: Email :: Post-Office',
          'Topic :: Communications :: Email :: Post-Office :: IMAP',
          'Intended Audience :: Developers',
          'Intended Audience :: Information Technology',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3.9'],
      python_requires='~=3.9',
      include_package_data=True,
      packages=find_packages(),
      install_requires=[
          'grpclib', 'protobuf', 'typing-extensions'],
      extras_require={
          'optional': ['googleapis-common-protos'],
          'build': ['grpcio-tools', 'mypy-protobuf']},
      entry_points={
          'console_scripts': [
              'pymap-admin = pymapadmin.main:main'],
          'pymapadmin.commands': [
              'save-args = pymapadmin.commands.system:SaveArgsCommand',
              'login = pymapadmin.commands.system:LoginCommand',
              'ping = pymapadmin.commands.system:PingCommand',
              'append = pymapadmin.commands.mailbox:AppendCommand',
              'get-user = pymapadmin.commands.user:GetUserCommand',
              'set-user = pymapadmin.commands.user:SetUserCommand',
              'delete-user = pymapadmin.commands.user:DeleteUserCommand'],
      })
