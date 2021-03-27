export const DownloadableImage = ({url, src, alt, download, ...props}) => {
    alt = alt || src;
    url = url || src;

    const onClick = () => {
        let a = document.createElement('a');
        a.href = url;
        a.download = download || url.split('/').pop();
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    };

    return (
        <img className="img-responsive clickable c-hand" src={src} alt={alt} onClick={onClick} {...props}/>
    )
};


const Image = ({src, alt, ...props}) => {
    alt = alt || src;

    return (
        <img className="img-responsive" src={src} alt={alt} {...props} />
    )
};


export const ImagesGrid = ({images, isClickable}) => {
    const Component = isClickable ? DownloadableImage : Image;

    const children = ['LU', 'RU', 'LL', 'RL'].map(key =>
        <div key={key} className="column col-6">
            <Component {...images[key]}/>
        </div>
    )

    return (
        <div className="container grid-lg images-grid">
            <div className="columns">
                {children}
            </div>
        </div>
    )
}