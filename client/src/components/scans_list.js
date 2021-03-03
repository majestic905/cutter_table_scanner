import {useCallback, useEffect} from "react";
import cx from 'classnames';
import folderSvg from "../images/folder-24px.svg";
import useFetch from "../hooks/useFetch";


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
    const [{isLoading, response, error}, doFetch] = useFetch("/api/scans");

    const doDelete = useCallback(() => {
        if (window.confirm('Точно удалить?'))
            doFetch({method: 'DELETE'});
    }, [onDelete]);

    useEffect(() => {
        if (response)
            onDelete();
        else if (error)
            alert(`Ошибка при удалении: ${error}`);
    }, [response, error]);

    const btnClassName = cx("btn btn-sm btn-primary", {loading: isLoading});

    return (
        <button type="button" className={btnClassName} onClick={doDelete}>
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