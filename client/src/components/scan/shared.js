import cx from "classnames";

export const Tab = ({text, active, name, onClick}) => {
    return (
        <li className={cx("tab-item text-tiny text-bold text-uppercase", {active})} data-tab-name={name} onClick={onClick}>
            <a href="#">{text}</a>
        </li>
    )
}

export const Tabs = ({activeTab, selectTab, children}) => {
    return (
        <ul className="tab tab-block">
            {children}
        </ul>
    )
}

export const ImagesGrid = ({images}) => {
    return (
        <div className="columns">
            <div className="column col-6">
                <img className="img-responsive" src={images['LU']} alt='LU'/>
            </div>
            <div className="column col-6">
                <img className="img-responsive" src={images['RU']} alt='RU'/>
            </div>
            <div className="column col-6">
                <img className="img-responsive" src={images['LL']} alt='LL'/>
            </div>
            <div className="column col-6">
                <img className="img-responsive" src={images['RL']} alt='RL'/>
            </div>
        </div>
    )
}