import {useCallback} from "react";
import cx from 'classnames';
import folderSvg from "../images/folder-24px.svg";


const Item = ({name, createdAt, isSelected, doSelect}) => {
    const className = cx({'text-bold': isSelected});

    return (
        <li>
            <span className={className} onClick={doSelect} data-name={name}>
                <img src={folderSvg} alt="folder_icon"/>
                <span>{createdAt}</span>
            </span>
        </li>
    )
}

const DeleteButton = ({onDelete}) => {
    const doDelete = useCallback(() => {
        if (window.confirm('Точно удалить?'))
            fetch('/api/scans', {method: 'DELETE'})
                .then(onDelete)
                .catch(error => console.error(error));
    }, [onDelete]);

    return (
        <span className='header-button' onClick={doDelete}>
            Удалить
        </span>
    )
}

const ScansList = ({scans, loadScans, selectedScan, selectScan}) => {
    const doSelect = useCallback(ev => {
        const name = ev.currentTarget.dataset.name;
        const scan = scans.find(item => item.name === name);
        selectScan(scan);
    }, [selectScan, scans]);

    if (!scans)
        return null;

    return (
        <div className="column col-2 no-scrollbar tree" id="column-file-tree">
            <h5 className="d-inline">Файлы</h5>
            <DeleteButton onDelete={loadScans} />

            <ul>
                {scans.map(item => <Item name={item.name}
                                         createdAt={item.createdAt}
                                         isSelected={item === selectedScan}
                                         doSelect={doSelect}
                />)}
            </ul>
        </div>
    )
}

export default ScansList;