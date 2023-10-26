from setuptools import setup

package_name = 'ir_camera'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='yansa',
    maintainer_email='yansa@todo.todo',
    description='Boson Infrared Camera Stream',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        'ir_pub = ir_camera.image_pub:main',
        'ir_sub = ir_camera.image_sub:main',
	'ir_grab = ir_camera.image_grab:main',
        ],
    },
)
