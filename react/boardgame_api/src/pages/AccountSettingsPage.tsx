import PageHeader from "../components/PageHeader.tsx";
import FormCard from "../components/FormCard.tsx";
import InputField from "../components/InputField.tsx";
import SubmitButton from "../components/SubmitButton.tsx";
import DangerCard from "../components/DangerCard.tsx";

function AccountSettingsPage() {

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
                            placeholder="MaxMustermann"
                            disabled={true}
                        />
                        <InputField
                            label="New Username"
                            type="text"
                            placeholder="Enter new Username"
                        />
                        <SubmitButton
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
                        <SubmitButton
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
                        <button className="btn btn-danger" onClick={handleDeleteUser}>
                            <i className="bi bi-trash-fill" /> Delete Account
                        </button>
                    </DangerCard>
                </div>
            </div>
        </div>
    );
}

export default AccountSettingsPage;