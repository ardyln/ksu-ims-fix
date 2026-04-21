rm -rf ims_source ims-fixed.apk tmp_ims ksu-ims-injection-v9.zip ims.apk uber-apk-signer.jar && cp /mnt/new_system_ext/priv-app/ims/ims.apk . && wget -q -O uber-apk-signer.jar https://github.com/patrickfav/uber-apk-signer/releases/download/v1.3.0/uber-apk-signer-1.3.0.jar && apktool d -r ims.apk -o ims_source && mkdir -p ims_source/smali/android/telephony && cat << 'EOF' > ims_source/smali/android/telephony/TelephonyBaseUtilsStub.smali
.class public Landroid/telephony/TelephonyBaseUtilsStub;
.super Ljava/lang/Object;
.method public constructor <init>()V
    .locals 0
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V
    return-void
.end method
.method public static getInstance()Landroid/telephony/TelephonyBaseUtilsStub;
    .locals 1
    new-instance v0, Landroid/telephony/TelephonyBaseUtilsStub;
    invoke-direct {v0}, Landroid/telephony/TelephonyBaseUtilsStub;-><init>()V
    return-object v0
.end method
.method public static isMiuiRom()Z
    .locals 1
    const/4 v0, 0x0
    return v0
.end method
EOF
apktool b ims_source -o ims-fixed.apk && java -jar uber-apk-signer.jar -a ims-fixed.apk --allowResign && mkdir -p tmp_ims/system/system_ext/priv-app/ims && cp ims-fixed-aligned-debugSigned.apk tmp_ims/system/system_ext/priv-app/ims/ims.apk && printf '%s\n' 'id=xiaomi_ims_injection9' 'name=Xiaomi IMS Native Injection V9' 'version=15.0' 'versionCode=15' 'author=ardy' 'description=Bakes class and patches SELinux rules for priv_app.' > tmp_ims/module.prop && cat << 'EOF' > tmp_ims/post-fs-data.sh
#!/system/bin/sh
MODDIR=${0%/*}
mount -o bind $MODDIR/system/system_ext/priv-app/ims/ims.apk /system_ext/priv-app/ims/ims.apk
rm -rf /data/dalvik-cache/*/*ims*
EOF
cat << 'EOF' > tmp_ims/sepolicy.rule
allow priv_app vendor_hal_telephony_service2 service_manager find
allow priv_app radio_service service_manager find
allow priv_app hal_telephony_hwservice hwservice_manager find
EOF
chmod 755 tmp_ims/post-fs-data.sh && cd tmp_ims && zip -rq9 ../ksu-ims-injection-v9.zip * && cd .. && rm -rf tmp_ims ims_source ims-fixed.apk ims.apk ims-fixed-aligned-debugSigned.apk 
echo -e "\n✅ Success! Flash ksu-ims-injection-v9.zip"
