import { useState } from 'react';
import { Box, Image, IconButton } from '@chakra-ui/react';
import { MdPhotoCamera } from 'react-icons/md';

function ProductPhotoBox() {
  const [imageUrl, setImageUrl] = useState('');

  const handleImageChange = event => {
    const file = event.target.files[0];
    const url = URL.createObjectURL(file);
    setImageUrl(url);
  };

  const handleCameraClick = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      const video = document.createElement('video');
      video.srcObject = stream;
      video.onloadedmetadata = () => {
        video.play();
        const canvas = document.createElement('canvas');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        const context = canvas.getContext('2d');
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        const dataURL = canvas.toDataURL('image/jpeg');
        setImageUrl(dataURL);
        stream.getTracks().forEach(track => track.stop());
      };
    } catch (error) {
      console.error(error);
      alert('Failed to access camera.');
    }
  };

  return (
    <Box position="relative" width={120} height={120}>
      <Image
        src={imageUrl}
        width={120}
        height={120}
        objectFit="cover"
        borderRadius="full" // ensures that the representation is a circle
        overflow="hidden" //what goes beyond the bound of component is cound
      />
      <input
        type="file"
        accept="image/*"
        onChange={handleImageChange}
        style={{ display: 'none' }}
      />
      <IconButton
        icon={<MdPhotoCamera />}
        position="absolute"
        bottom={0}
        right={0}
        size="sm"
        onClick={handleCameraClick}
      />
    </Box>
  );
}

export default ProductPhotoBox;
