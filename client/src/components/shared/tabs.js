import cx from "classnames";

export const Tab = ({text, isActive, name, onClick}) => {
    const className = cx("tab-item text-bold text-uppercase", {active: isActive});
    return (
        <li className={className} data-tab-name={name} onClick={onClick}>
            <a href="#">{text}</a>
        </li>
    )
}

export const Tabs = ({children}) => {
    return (
        <ul className="tab">
            {children}
        </ul>
    )
}