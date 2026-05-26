import PageHeader from "../components/PageHeader.tsx";
import FormCard from "../components/FormCard.tsx";
import InputField from "../components/InputField.tsx";
import Button from "../components/Button.tsx";
import DangerCard from "../components/DangerCard.tsx";
import {useContext, useState} from "react";
import {AuthContext} from "../context/AuthContext.tsx";
import ConfirmModal from "../components/ConfirmModal.tsx";
import type {InfoText} from "../types/InfoText.ts";
import InformationText from "../components/InformationText.tsx";
import {getDetailStringOrDefault} from "../util/util.ts";
import {useNavigate} from "react-router-dom";
import PageContainer from "../components/PageContainer.tsx";

function AccountSettingsPage() {

    const navigate = useNavigate();

    const { user, setUser } = useContext(AuthContext)!;

    const [newUsername, setNewUsername] = useState("");
    const [oldPassword, setOldPassword] = useState("");
    const [newPassword, setNewPassword] = useState("");
    const [newPasswordConfirm, setNewPasswordConfirm] = useState("");
    const [changeUsernameInfo, setChangeUsernameInfo] = useState<InfoText>({message: ""});
    const [changePasswordInfo, setChangePasswordInfo] = useState<InfoText>({message: ""});
    const [deleteAccountInfo, setDeleteAccountInfo] = useState<InfoText>({message: ""});


    const handleChangeUsername = async () => {
        const response = await fetch(`/api/user/${user?.id}/username`, {
            method: "PATCH",
            credentials: "include",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({new_username: newUsername})
        });

        const data = await response.json();
        if (response.ok) {
            setUser({id: data.id, name: data.name});
            setChangeUsernameInfo({message: data.message, variant:"success"})
        }
        else {
            setChangeUsernameInfo({message: getDetailStringOrDefault(data.detail, "Unknown error"), variant:"warning"})
        }
    };

    const handleChangePassword = async ()  => {
        const passwords = {
            oldPassword: oldPassword,
            newPassword: newPassword
        };

        const response = await fetch(`/api/user/${user?.id}/password`, {
            method: "PATCH",
            credentials: "include",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(passwords)
        });

        const data = await response.json();
        if (response.ok) {
            setChangePasswordInfo({message: data.message, variant:"success"})
        }
        else {
            setChangePasswordInfo({message: getDetailStringOrDefault(data.detail, "Unknown error"), variant:"warning"})
        }
        setOldPassword("")
        setNewPassword("")
        setNewPasswordConfirm("")
    };

    const handleDeleteUser = async () => {
        const response = await fetch(`/api/user/${user?.id}`, {
            method: "DELETE",
            credentials: "include",
            headers: {"Content-Type": "application/json"},

        });

        const data = await response.json();
        if (response.ok) {
            setDeleteAccountInfo({message: data.message, variant:"success"})

            setTimeout(() => {
                navigate("/login");
            }, 3000)
        }
        else {
            setDeleteAccountInfo({message: getDetailStringOrDefault(data.detail, "Unknown error"), variant: "warning"})
        }
    };

    return (
        <PageContainer>
            <PageHeader header={<><i className="bi bi-gear-fill" /> Account Settings</>} subHeader="Manage your account information and security settings." />

            {/* Change Username */}
            <FormCard header={<><i className="bi bi-person-fill" /> Change Username</>}>
                <InputField
                    label="Current Username"
                    type="text"
                    value={user?.name}
                    disabled={true}
                />
                <InputField
                    label="New Username"
                    type="text"
                    placeholder="Enter new Username"
                    value={newUsername}
                    onChange={(e) => setNewUsername(e.target.value)}
                />
                <InformationText infoText={changeUsernameInfo} />
                <Button
                    variant="primary"
                    label={<><i className="bi bi-check-lg" /> Save Username</>}
                    onClick={handleChangeUsername}
                    disabled={!newUsername}
                />
            </FormCard>

            {/* Change Password */}
            <FormCard header={<><i className="bi bi-key-fill" /> Change Password</>}>
                <InputField
                    label="Current Password"
                    type="password"
                    placeholder="Enter current password"
                    value={oldPassword}
                    onChange={(e) => setOldPassword(e.target.value)}
                />
                <InputField
                    label="New Password"
                    type="password"
                    placeholder="Enter new password"
                    value={newPassword}
                    onChange={(e) => setNewPassword(e.target.value)}
                />
                <InputField
                    label="Confirm New Password"
                    type="password"
                    placeholder="Confirm new password"
                    value={newPasswordConfirm}
                    onChange={(e) => setNewPasswordConfirm(e.target.value)}
                />
                <InformationText infoText={changePasswordInfo} />
                <Button
                    variant="primary"
                    label={<><i className="bi bi-check-lg" /> Save Password</>}
                    onClick={handleChangePassword}
                />
            </FormCard>

            {/* Danger Zone */}
            <ConfirmModal id="confirmAccountDeleteModal" header="Are you sure?" body="Deleting you Account deletes all data irrevocable." onSubmit={handleDeleteUser} />
            <DangerCard header="Danger Zone">
                <p className="text-body-secondary">
                        Deleting your account is permanent and cannot be undone.
                        All your data will be lost.
                </p>
                <InformationText infoText={deleteAccountInfo} />
                <Button
                    variant="danger"
                    label={<><i className="bi bi-trash-fill" /> Delete Account</>}
                    data-bs-toggle="modal"
                    data-bs-target="#confirmAccountDeleteModal"
                />
            </DangerCard>
        </PageContainer>
    );
}

export default AccountSettingsPage;