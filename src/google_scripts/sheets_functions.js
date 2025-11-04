function getStatusCode(url){
   var options = {
     'muteHttpExceptions': true,
     'followRedirects': false
   };
   var url_trimmed = url.trim();
   var response = UrlFetchApp.fetch(url_trimmed, options);
   return response.getResponseCode();
}

function getImageMegabytesFromUrl(imageUrl) {
  if (!imageUrl || typeof imageUrl !== 'string' || !imageUrl.startsWith('http')) {
    return "Invalid URL provided";
  }

  try {
    // Fetch the image data from the URL
    var response = UrlFetchApp.fetch(imageUrl);
    
    // Get the image data as a Blob
    var imageBlob = response.getBlob();
    
    // Get the raw bytes array
    var imageBytes = imageBlob.getBytes();
    
    // The length of the byte array is the size in bytes
    var byteSize = imageBytes.length;
    
    // Convert bytes to megabytes (1 MB = 1024 * 1024 bytes)
    var megaByteSize = byteSize / (1024 * 1024);
    
    // Round to 2 decimal places for easier reading
    megaByteSize = Math.round(megaByteSize * 100) / 100;
    
    return megaByteSize;

  } catch (e) {
    return "Error fetching image: " + e.message;
  }
}