import cx from "classnames";

export const Tab = ({text, isActive, name, onClick}) => {
    const className = cx("tab-item text-tiny text-bold text-uppercase", {active: isActive});
    return (
        <li className={className} data-tab-name={name} onClick={onClick}>
            <a href="#">{text}</a>
        </li>
    )
}

export const Tabs = ({children}) => {
    return (
        <ul className="tab tab-block">
            {children}
        </ul>
    )
}

const ClickableImage = ({filename, url, src, alt, ...props}) => {
    alt = alt || src;
    url = url || src;

    if (!filename) {
        const pathItems = src.split('/');
        filename = pathItems[pathItems.length - 1];
    }

    const doDownloadFile = useCallback(() => {
        fetch(url)
          .then(resp => resp.blob())
          .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
          })
          .catch(error => {
              console.error(error);
              alert(error.message);
          });
    }, [url, filename]);

    return (
        <img className="img-responsive c-hand" src={src} alt={alt} onClick={doDownloadFile}/>
    )
}


const Image = ({src, alt, ...props}) => {
    alt = alt || src;

    return (
        <img className="img-responsive" src={src} alt={alt} {...props} />
    )
};


export const ImagesGrid = ({images, isClickable}) => {
    const Component = isClickable ? ClickableImage : Image;

    const children = ['LU', 'RU', 'LL', 'RL'].map(key =>
        <div className="column col-6">
            <Component {...images[key]}/>
        </div>
    )

    return (
        <div className="columns">
            {children}
        </div>
    )
}