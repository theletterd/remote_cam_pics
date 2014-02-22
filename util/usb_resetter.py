import usb

def reset_usb(camera_manufacturer):
    all_usb_devices = usb.core.find(find_all=True)

    for device in all_usb_devices:
        try:
            device_product = usb.util.get_string(device, 256, device.iProduct)
            if camera_manufacturer.lower() in device_product.lower():
                device.reset()
                return
        except:
            pass

