import {useState, useEffect} from "react";
import Directory from "./directory";

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

const FileTree = () => {
    const [directories, setDirectories] = useState(null);

    useEffect(() => {
        fetch('/api/files')
            .then(res => res.json())
            .then(data => setDirectories(data));
    }, []);

    if (directories)
        return (
            <div className="column no-scrollbar tree" id="column-file-tree">
                <div>
                    <h5 className="d-inline">Файлы</h5>
                    <span id="button-delete" className="text-uppercase text-tiny">Удалить</span>
                </div>

                <ul>
                    {directories.map(directory => <Directory tree={directory} />)}
                </ul>
            </div>
        )

    return null;
}

export default FileTree;