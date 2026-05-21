import PageHeader from "../components/PageHeader.tsx";
import FormCard from "../components/FormCard.tsx";
import InputField from "../components/InputField.tsx";
import Button from "../components/Button.tsx";
import DangerCard from "../components/DangerCard.tsx";
import {useContext, useState} from "react";
import {AuthContext} from "../context/AuthContext.tsx";
import ConfirmModal from "../components/ConfirmModal.tsx";

function AccountSettingsPage() {

    const { user } = useContext(AuthContext)!;

    const [newUsername, setNewUsername] = useState("");
    const [oldPassword, setOldPassword] = useState("");
    const [newPassword, setNewPassword] = useState("");
    const [newPasswordConfirm, setNewPasswordConfirm] = useState("");


    const handleChangeUsername = async () => {

    };

    const handleChangePassword = async ()  => {};

    const handleDeleteUser = async () => {};

    return (
        <div className="container py-5">
            <div className="row justify-content-center">
                <div className="col-12 col-lg-8">

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
                        <Button
                            variant="danger"
                            label={<><i className="bi bi-trash-fill" /> Delete Account</>}
                            data-bs-toggle="modal"
                            data-bs-target="#confirmAccountDeleteModal"
                        />
                    </DangerCard>
                </div>
            </div>
        </div>
    );
}

export default AccountSettingsPage;