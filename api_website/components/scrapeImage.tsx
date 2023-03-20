import Image from 'next/image';
export interface ImageProps {
  url: string;
  name: string;
}

export function GetImage({url, name}: ImageProps)  { 
  //(?:sku=)\d+(?:&)
  console.log( "clown" )
  const regex = /(sku=)\d+/g;
  console.log(url.match( regex ))
  const matches = url.match( regex );
  
  const src = 'https://media.ulta.com/i/ulta/'+matches?.[0].slice(4)+'?w=1080'
  console.log( src );
  return (
  <Image src={src} alt= {name} width={200} height={200}>
  </Image> 
  );
}
