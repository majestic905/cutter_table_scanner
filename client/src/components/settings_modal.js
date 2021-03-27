import {useCallback, useEffect, useState} from "react";
import useFetch from "../hooks/useFetch";
import cx from "classnames";


const CamerasColumns = ({cameras}) => {
    return (
        <div id="cameras" className="columns">
            <div className="column col-6">
                <label className="form-label text-bold" htmlFor="camera-LU">LU: Left Upper</label>
                <textarea id="camera-LU" name="LU" className="form-input" defaultValue={cameras['LU']}/>
            </div>
            <div className="column col-6">
                <label className="form-label text-bold" htmlFor="camera-RU">RU: Right Upper</label>
                <textarea id="camera-RU" name="RU" className="form-input" defaultValue={cameras['RU']}/>
            </div>
            <div className="column col-6">
                <label className="form-label text-bold" htmlFor="camera-LL">LL: Left Lower</label>
                <textarea id="camera-LL" name="LL" className="form-input" defaultValue={cameras['LL']}/>
            </div>
            <div className="column col-6">
                <label className="form-label text-bold" htmlFor="camera-RL">RL: Right Lower</label>
                <textarea id="camera-RL" name="RL" className="form-input" defaultValue={cameras['RL']}/>
            </div>
        </div>
    )
}


const SettingsModal = ({closeModal}) => {
    const [data, setData] = useState();

    const [{isLoading, response, error}, doFetch] = useFetch('/api/cameras');  // for both GET and POST

    useEffect(doFetch, [doFetch]);

    useEffect(() => {
        if (response !== undefined && !data) { // GET
            setData(response);
        } else if (response !== undefined && data) // POST
            closeModal();
    }, [response, setData, closeModal]);

    const doSubmit = useCallback(ev => {
        ev.preventDefault();

        const body = {};
        for (const position of ['LU', 'LL', 'RL', 'RU'])
            body[position] = ev.target.elements[position].value;


        doFetch({
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        });
    }, [doFetch]);

    const btnClassName = cx("btn btn-primary float-right mr-2", {loading: isLoading});

    return (
        <form className="modal active" onSubmit={doSubmit}>
            <span className="modal-overlay" onClick={closeModal}/>
            <div className="modal-container modal-fullheight">
                <div className="modal-header">
                    <button type="button" className="btn btn-link float-right" onClick={closeModal}>Закрыть</button>
                    <input type="submit" className={btnClassName} value="Отправить"/>

                    <div className="modal-title h5">Настройки</div>
                </div>
                <ul className="mt-0">
                   <li className="mt-0">
                       Значения table_section_size (миллиметры) напрямую в программе не используются, они здесь для того чтобы были.
                   </li>
                   <li className="mt-0">
                       Значения projected_image_size (пиксели) используются; задаются вручную; должны быть строго пропорциональны значениям table_section_size!
                   </li>
               </ul>
                {error && <div className="modal-header pt-0">
                     <div className="toast toast-error">{error}</div>
                </div>}
                <div className="modal-body pt-0">
                    {data && <CamerasColumns cameras={data}/>}
                    {isLoading && <div className="loading loading-lg"/>}
                </div>
            </div>
        </form>
    )
};


export default SettingsModal;