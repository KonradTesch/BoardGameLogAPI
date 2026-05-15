import PageHeader from "../components/PageHeader.tsx";
import FormCard from "../components/FormCard.tsx";
import InputField from "../components/InputField.tsx";
import Button from "../components/Button.tsx";
import DangerCard from "../components/DangerCard.tsx";
import {useContext} from "react";
import {AuthContext} from "../context/AuthContext.tsx";

function AccountSettingsPage() {

    const { user } = useContext(AuthContext)!;

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
                        />
                        <Button
                            variant="primary"
                            label={<><i className="bi bi-check-lg" /> Save Username</>}
                            onClick={handleChangeUsername}
                        />
                    </FormCard>

                    {/* Change Password */}
                    <FormCard header={<><i className="bi bi-key-fill" /> Change Password</>}>
                        <InputField
                            label="Current Password"
                            type="password"
                            placeholder="Enter current password"
                        />
                        <InputField
                            label="New Password"
                            type="password"
                            placeholder="Enter new password"
                        />
                        <InputField
                            label="Confirm New Password"
                            type="password"
                            placeholder="Confirm new password"
                        />
                        <Button
                            variant="primary"
                            label={<><i className="bi bi-check-lg" /> Save Password</>}
                            onClick={handleChangePassword}
                        />
                    </FormCard>

                    {/* Danger Zone */}
                    <DangerCard header="Danger Zone">
                        <p className="text-body-secondary">
                                Deleting your account is permanent and cannot be undone.
                                All your data will be lost.
                        </p>
                        <Button
                            variant="danger"
                            label={<><i className="bi bi-trash-fill" /> Delete Account</>}
                            onClick={handleDeleteUser}>
                        </Button>
                    </DangerCard>
                </div>
            </div>
        </div>
    );
}

export default AccountSettingsPage;