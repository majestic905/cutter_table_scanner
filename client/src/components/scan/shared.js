import cx from "classnames";
import {useCallback} from "react";

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

export const ClickableImage = ({filename, url, src, alt, ...props}) => {
    alt = alt || src;
    url = url || src;

    if (!filename && url) {
        const pathItems = url.split('/');
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
        <img className="img-responsive clickable c-hand" src={src} alt={alt} onClick={doDownloadFile} {...props}/>
    )
};


const Image = ({src, alt, ...props}) => {
    alt = alt || src;

    return (
        <img className="img-responsive" src={src} alt={alt} {...props} />
    )
};


export const ImagesGrid = ({images, isClickable}) => {
    const Component = isClickable ? ClickableImage : Image;

    const children = ['LU', 'RU', 'LL', 'RL'].map(key =>
        <div key={key} className="column col-6">
            <Component {...images[key]}/>
        </div>
    )

    return (
        <div className="container grid-xs">
            <div className="columns">
                {children}
            </div>
        </div>
    )
}