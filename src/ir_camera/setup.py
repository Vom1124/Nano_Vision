from setuptools import find_packages, setup

package_name = 'ir_camera'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='vom',
    maintainer_email='vomsheendhur@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        'ir_pub = ir_camera.image_pub:main',
        'ir_sub = ir_camera.image_sub:main',
	    'ir_grab = ir_camera.image_grab:main',
        ],
    },
)
