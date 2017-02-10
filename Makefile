build_image:
	echo "building..."
	docker build -t remote_cam_pics .

stop_container:
	echo "stopping"
	docker ps -f ancestor=remote_cam_pics -q | xargs docker stop

clean:
	echo "cleaning..."
	docker rmi remote_cam_pics -f

start_container:
	echo "Starting container..."
	docker run -d -p 8000:8000 --privileged -v $(CURDIR)/static/originals/:/app/static/originals/ -v /dev/bus/usb:/dev/bus/usb remote_cam_pics
