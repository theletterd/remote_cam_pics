stop_container:
	echo "stopping"
	docker ps -f ancestor=remote_cam_pics -q | xargs --no-run-if-empty docker stop

clean: stop_container
	echo "cleaning..."
	docker rmi remote_cam_pics -f

build_image: clean
	echo "building..."
	docker build -t remote_cam_pics .

start_container:
	echo "Starting container..."
	docker run -d -p 8000:8000 --privileged -v $(CURDIR)/static/originals/:/app/static/originals/ -v /dev/bus/usb:/dev/bus/usb remote_cam_pics
