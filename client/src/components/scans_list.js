import {useCallback} from "react";
import cx from 'classnames';
import folderSvg from "../images/folder-24px.svg";


const Item = ({item, createdAt, isSelected, doSelect}) => {
    const className = cx({'text-bold': isSelected});

    return (
        <li>
            <span className={className} onClick={doSelect} data-id={item.scanId}>
                <img src={folderSvg} alt="folder_icon"/>
                <span>{item.createdAt} ({item.scanType[0]})</span>
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
        <button type="button" className='btn btn-sm bg-dark' onClick={doDelete}>
            Удалить все
        </button>
    )
}

const ScansList = ({scans, loadScans, selectedScan, selectScan}) => {
    const doSelect = useCallback(ev => {
        const id = ev.currentTarget.dataset.id;
        const scan = scans.find(item => item.scanId === id);
        selectScan(scan);
    }, [selectScan, scans]);

    if (!scans)
        return null;

    return (
        <div className="tree" id="scans-list">
            <header>
                <DeleteButton onDelete={loadScans} />
            </header>

            <hr/>

            <ul>
                {scans.map(item => <Item key={item.scanId}
                                         item={item}
                                         isSelected={item === selectedScan}
                                         doSelect={doSelect}
                />)}
            </ul>
        </div>
    )
}

export default ScansList;