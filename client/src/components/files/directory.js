import React, {useState} from "react";
import cx from "classnames";
import fileSvg from "../../images/receipt-24px.svg";
import folderSvg from "../../images/folder-24px.svg";
import folderOpenSvg from "../../images/folder_open-24px.svg";


const File = ({file}) => {
    return (
        <li>
            <span>
                <img src={fileSvg} alt={file.name}/>
                <span>{file.name}</span>
            </span>
        </li>
    )
}

const Directory = ({tree}) => {
    const [isOpened, setIsOpened] = useState(false);

    if (tree.type === "F") {
        return <File file={tree}/>;
    }

    return (
        <li className={cx({opened: isOpened})}>
            <span onClick={() => setIsOpened((value) => !value)}>
                <img src={isOpened ? folderOpenSvg : folderSvg} alt={tree.name}/>
                <span>{tree.name}</span>
            </span>
            {isOpened && 
                <ul>
                    {tree.children.map(child => <Directory key={child.name} tree={child}/>)}
                </ul>
            }
        </li>
    )
}

export default Directory;