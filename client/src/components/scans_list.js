import {useState, useEffect, useCallback} from "react";
import cx from 'classnames';
import folderSvg from "../images/folder-24px.svg";

// const response = {
//     type: "D",
//     name: "storage",
//     children: [
//         {
//             type: "D",
//             name: "03a2fd11-d5d6-40f5-8b8d-5cf1ac7b4ece",
//             children: [
//                 {
//                     type: "F",
//                     name: "RIPEngine.xml",
//                     mtime: "2020-01-30T12:22:36.524Z",
//                     size: 174701,
//                   }
//             ]
//         }
//     ]
// }

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

const CreateButton = ({onCreate}) => {
    const doCreate = useCallback(() => {
        fetch('/api/scans', {method: 'POST'})
            .then(onCreate)
    }, []);

    return (
        <span id="button-delete" onClick={doCreate}>
            Создать
        </span>
    )
}

const DeleteButton = ({onDelete}) => {
    const doDelete = useCallback(() => {
        if (window.confirm('Точно удалить?'))
            fetch('/api/scans', {method: 'DELETE'})
                .then(onDelete)
    }, []);

    return (
        <span id="button-delete" onClick={doDelete}>
            Удалить
        </span>
    )
}

const ScansList = ({size, selectedScan, selectScan}) => {
    const [scans, setScans] = useState(null);

    const loadScans = useCallback(() => {
        fetch('/api/scans')
            .then(res => res.json())
            .then(data => setScans(data.scans));
    }, [setScans]);

    useEffect(loadScans, []);

    const doSelect = useCallback(ev => {
        const name = ev.currentTarget.dataset.name;
        const scan = scans.find(item => item.name === name);
        selectScan(scan);
    }, [selectScan, scans]);

    if (!scans)
        return null;

    return (
        <div className={`column col-${size} no-scrollbar tree`} id="column-file-tree">
            <h5 className="d-inline">Файлы</h5>
            <CreateButton onCreate={loadScans} />
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